from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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

@router.get("/dashboard/statistics", response_model=schemas.DashboardStats)
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    stats = crud.get_dashboard_stats(db)
    return stats
