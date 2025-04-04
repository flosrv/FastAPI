from sqlalchemy.orm import Session
from models import  User as UserModel
from schemas import User as UserSchema, UserCreate
from datetime import timedelta, datetime
from jose import jwt, JWTError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

SECRET_KEY = "mySecretKey"

EXPIRE_DELAY_MINUTES = 60 * 24 * 7 # One week
ALGORITHM = "HS256"

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token") # => localhost:800/token
bcrypt_context = CryptContext(schemes=["bcrypt"])

async def existing_user(db: Session,  username:str, email:str):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user:
        return db_user
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if db_user:
        return db_user
    return None

#create token
async def create_access_token(id:int, username:str):
            encode = {"sub": username, "id": id}
            expires = datetime.utcnow() +timedelta(minutes=EXPIRE_DELAY_MINUTES)
            encode.update({"exp": expires})
            return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# get_current_user from token
async def get_current_user(db:Session, token:Depends):

    try:
          payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

          username:str = payload.get("sub")
          id:int = payload.get("id")
          expire : datetime =payload.get("exp")
          if expire < datetime.utcnow():
                return None
          if username is None or id is None:
                return None
          db_user = db.query(UserModel).filter(UserModel.username == username).first()
          return db_user
    except JWTError:
          return None

# Create User
async def create_user(db:Session, user: UserCreate):
    db_user = UserModel(
          username = user.username,
          email = user.email,
          hashed_pasword = bcrypt_context.hash(user.password),)
    db.add(db_user)
    db.commit()
    return db_user






























