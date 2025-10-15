from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import crud, models, schemas
from ..database import SessionLocal
from .users import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads", response_model=schemas.Lead)
def create_lead(
    lead: schemas.LeadCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    return crud.create_lead(db=db, lead=lead)

@router.get("/leads", response_model=List[schemas.Lead])
def read_leads(
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None, 
    status: Optional[str] = None, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    leads = crud.get_leads(db, skip=skip, limit=limit, search=search, status=status)
    return leads

@router.get("/leads/{lead_id}", response_model=schemas.Lead)
def read_lead(
    lead_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_lead = crud.get_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.put("/leads/{lead_id}", response_model=schemas.Lead)
def update_lead(
    lead_id: int, 
    lead: schemas.LeadCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_lead = crud.update_lead(db, lead_id=lead_id, lead=lead)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.delete("/leads/{lead_id}", response_model=schemas.Lead)
def delete_lead(
    lead_id: int, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    db_lead = crud.delete_lead(db, lead_id=lead_id)
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead
