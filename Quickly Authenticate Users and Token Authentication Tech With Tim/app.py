from datetime import datetime, timezone, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from models import User as UserModel
from schemas import User as UserSchema, UserCreate
from database import get_db
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import services

app =FastAPI()

@app.post("signup", status_code=status.HTTP_201_CREATED)
async def create_user(user:UserCreate,db: Session = Depends(get_db) ):

    db_user = services.existing_user(db, user.username, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                            detail="username or email already exists")
    
    await services.create_user(db,user)
    access_token = await services.create_access_token(db_user.id, db_user.username)
    return {"access_token": access_token,
            "token_type": "bearer",
            "username": db_user.username,
            }    

