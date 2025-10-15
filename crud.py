from sqlalchemy.orm import Session
from typing import Optional

from . import models, schemas, security

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Lead CRUD functions
def create_lead(db: Session, lead: schemas.LeadCreate):
    db_lead = models.Lead(**lead.dict())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads(db: Session, skip: int = 0, limit: int = 10, search: Optional[str] = None, status: Optional[str] = None):
    query = db.query(models.Lead).filter(models.Lead.is_active == True)
    if search:
        query = query.filter(
            (models.Lead.first_name.ilike(f"%{search}%")) |
            (models.Lead.last_name.ilike(f"%{search}%")) |
            (models.Lead.email.ilike(f"%{search}%"))
        )
    if status:
        query = query.filter(models.Lead.status == status)
    return query.offset(skip).limit(limit).all()

def get_lead(db: Session, lead_id: int):
    return db.query(models.Lead).filter(models.Lead.id == lead_id, models.Lead.is_active == True).first()

def update_lead(db: Session, lead_id: int, lead: schemas.LeadCreate):
    db_lead = get_lead(db, lead_id)
    if db_lead:
        for key, value in lead.dict(exclude_unset=True).items():
            setattr(db_lead, key, value)
        db.commit()
        db.refresh(db_lead)
    return db_lead

def delete_lead(db: Session, lead_id: int):
    db_lead = get_lead(db, lead_id)
    if db_lead:
        db_lead.is_active = False
        db.commit()
        db.refresh(db_lead)
    return db_lead
