from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id=Column(Integer, primary_key =True)
    username= Column(String, unique=True, index=True)
    email= Column(unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    created_dt = Column(DateTime, default=datetime.utcnow())
