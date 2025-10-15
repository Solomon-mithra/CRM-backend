from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import date, timedelta
from sqlalchemy import func

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

# Activity CRUD functions
def create_lead_activity(db: Session, activity: schemas.ActivityCreate, lead_id: int, user_id: int):
    db_activity = models.Activity(**activity.dict(), lead_id=lead_id, user_id=user_id)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_lead_activities(db: Session, lead_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Activity).options(joinedload(models.Activity.user)).filter(models.Activity.lead_id == lead_id).offset(skip).limit(limit).all()

# Dashboard CRUD functions
def get_dashboard_stats(db: Session):
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    total_leads = db.query(models.Lead).filter(models.Lead.is_active == True).count()
    new_leads_this_week = db.query(models.Lead).filter(models.Lead.created_at >= start_of_week).count()
    closed_leads_this_month = db.query(models.Lead).filter(models.Lead.status == "closed", models.Lead.updated_at >= start_of_month).count()
    total_activities = db.query(models.Activity).count()

    leads_by_status = db.query(models.Lead.status, func.count(models.Lead.id)).group_by(models.Lead.status).all()

    recent_activities = db.query(models.Activity).order_by(models.Activity.created_at.desc()).limit(10).all()

    return {
        "total_leads": total_leads,
        "new_leads_this_week": new_leads_this_week,
        "closed_leads_this_month": closed_leads_this_month,
        "total_activities": total_activities,
        "leads_by_status": [{"status": status, "count": count} for status, count in leads_by_status],
        "recent_activities": recent_activities,
    }
