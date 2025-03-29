from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from config import Settings
from sqlalchemy.orm import declarative_base

# Initialize settings object
settings = Settings()

# Create the database engine using the DATABASE_URL from settings
engine = AsyncEngine(
    create_engine(
        url=C
        
# Base class for all models
Base = declarative_base()

# SessionLocal is used to create database sessions for interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
