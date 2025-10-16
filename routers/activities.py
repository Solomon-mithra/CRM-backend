from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import SessionLocal
from routers.users import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/leads/{lead_id}/activities", response_model=schemas.Activity)
def create_activity_for_lead(
    lead_id: int,
    activity: schemas.ActivityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return crud.create_lead_activity(db=db, activity=activity, lead_id=lead_id, user_id=current_user.id)

@router.get("/leads/{lead_id}/activities", response_model=List[schemas.Activity])
def read_lead_activities(
    lead_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    activities = crud.get_lead_activities(db, lead_id=lead_id, skip=skip, limit=limit)
    return activities
