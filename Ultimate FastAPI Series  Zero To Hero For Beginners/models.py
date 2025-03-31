from pydantic import BaseModel, Field
from fastapi import FastAPI, Query, Path
from typing import Optional, Annotated

class BaseUser(BaseModel):
    username:str
    name:str
    email: str

class UserIn(BaseUser):
    password:str

class UserOut(BaseUser):
    pass

class UserInDB(BaseUser):
    hashed_password: str


class Image(BaseModel):
    url:str
    name:str

class Item(BaseModel):
    name:str
    description:Optional[str] = None, 
    Field(default=None, 
            description= "description of the item",
            max_length=10)
    price:float
    tax:Optional[float] = None
    tags : set[str] = set()
    image : Optional[list[Image]] = None
