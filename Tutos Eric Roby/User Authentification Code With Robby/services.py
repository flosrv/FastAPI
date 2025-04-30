from sqlalchemy.orm import Session
from models.users import User as UserModel
from schemas.users import User as UserSchema, UserBase, UserCreate
from datetime import timedelta, datetime
from jose import jwt, JWTError, cryptography
from passlib import bcrypt



secret_KEY = "your_secret_key"
ALGORITHM = "HS256"
EXPIRE_TIME = timedelta(minutes=60*24)

 # check existing user with same username or email
async def check_existing_user(db: Session, username_or_email: str) -> bool:
     db_user = db.query(UserModel).filter(UserModel.username == username_or_email).first() 
     
     if db_user:
          return db_user
     db_user = db.query(UserModel).filter(UserModel.email == username_or_email).first()
     if db_user:
            return db_user


## token creation
async def create_access_token(data: dict, 
                              expires_delta: timedelta = timedelta(minutes=30)) -> str:

    encode = jwt.encode(data, secret_KEY, algorithm=ALGORITHM)
    expires_delta = datetime.utc.now() + expires_delta

## authenticate user
