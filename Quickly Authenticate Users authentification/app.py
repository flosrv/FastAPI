from datetime import datetime, timezone, timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

# Secret key used for encoding and decoding JWT tokens
SECRET_KEY = "$2b$12$zGyTNLJmVKRUWadG2GpQge2g9VcHLkX0WaPPtUxtJ9aixXshXLdLu"

# Algorithm used for JWT encoding
ALGORITHM = "HS256"

# Token expiration time in minutes
ACCESS_TOKEN_EXPIRES_MINUTES = 30

# Simulated database for demonstration purposes
db = {
    "flo": {
        "username": "flo",
        "email": "flo@gmail.com",
        "hashed_password": "$2b$12$vkI36aPo0ef91HnqkT67ZOSgPhOaZ9T.QDUmaN8AOM21QiN5AmCvq", 
        "disabled": False
    }
}

# Pydantic models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel): 
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class Data(BaseModel):
    name: str

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme for authentication
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Function to verify a password
def verify_pwd(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a password
def get_pwd_hash(password):
    return pwd_context.hash(password)

# Function to retrieve a user from the database
def get_user(db, username: str):
    user_data = db.get(username)
    if user_data:
        return UserInDB(**user_data)
    return None

# Function to authenticate a user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user or not verify_pwd(password, user.hashed_password):
        return False
    return user

# Function to create a JWT token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Function to get the current user
async def get_current_user(token: str = Depends(oauth_2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception

    return user

# Function to get the current active user
async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

# Initialize FastAPI
app = FastAPI()

# Test endpoint
@app.get("/{item_id}/")
async def test(item_id: str, query: int = 1):
    return {'hello': item_id}

# Create endpoint
@app.post("/create")
async def create(data: Data):
    return {"data": data}

# Token endpoint for authentication
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get current user endpoint
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Get user items endpoint
@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": 1, "owner": current_user.username}]
