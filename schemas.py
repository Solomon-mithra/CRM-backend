from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional, Dict, Any

# Token Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# User Models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str

class User(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

# Lead Models
class LeadCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    status: str = "new"
    source: str = "website"
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    property_interest: Optional[str] = None

class Lead(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    status: str
    source: str
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    property_interest: Optional[str] = None
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    activity_count: int = 0

    class Config:
        from_attributes = True

# Activity Models
class ActivityCreate(BaseModel):
    activity_type: str # call/email/meeting/note
    title: str
    notes: Optional[str] = None
    duration: Optional[int] = None # minutes
    activity_date: date

class Activity(BaseModel):
    id: int
    lead_id: int
    user_id: int
    activity_type: str
    title: str
    notes: Optional[str] = None
    duration: Optional[int] = None
    activity_date: date
    created_at: datetime
    user_name: str

    class Config:
        from_attributes = True

# Dashboard Model
class DashboardStats(BaseModel):
    total_leads: int
    new_leads_this_week: int
    closed_leads_this_month: int
    total_activities: int
    leads_by_status: List[Dict[str, Any]]
    recent_activities: List[Activity]
