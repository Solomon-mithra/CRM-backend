import os
from dotenv import load_dotenv
from fastapi import FastAPI
from database import engine, Base
from routers import users, leads, activities, dashboard
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file for local development
load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Set up CORS using an environment variable.
# Defaulting to standard frontend development ports (Vite, Create React App).
# In production, you should set CORS_ORIGINS to your frontend's URL.
CORS_ORIGINS = os.getenv("CORS_ORIGINS")
origins = [origin.strip() for origin in CORS_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api")
app.include_router(leads.router, prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRM API"}