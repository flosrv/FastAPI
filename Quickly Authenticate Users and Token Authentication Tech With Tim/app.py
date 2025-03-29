from datetime import datetime, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional


SECRET_KEY="ffb723b2f570c1b503dc6374e34373eda3b6999e25dab50139415e211ee05e1c"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 30

fake_db= {
    "username":"flo",
    "email": "flo@gmail.com",
     "hashed_pasword": "",
     "disabled":False
}


class Token(BaseModel):
    access_token:str
    token_type:str




class TokenData(BaseModel): 
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disable: Optional[bool] = None


class UserInDB(User):
    hashed_password:str

class Data(BaseModel):
    name:str

pwd_context = CryptContext(schemes=["bcrypt"], 
                           deprecated="auto")

oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# "hello" -> "rnerkgegtrhntrkjlhthr"

def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_pwd_hash(password):
    return pwd_context.hash(password)

def get_user(db, username : str):
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)

def authenticate_user(db, username:str, password:str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_pwd(password,user.hashed_password) :
        return False
    return user

def create_access_token(data:dict, expires_delta: Optional[timedelta]=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=50)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt











app = FastAPI()
@app.get("/{item_id}/")
async def test(item_id : str, query : int = 1):
    return {'hello': item_id}


@app.post("/create")
async def create(data : Data):
    return {"data" : data}



