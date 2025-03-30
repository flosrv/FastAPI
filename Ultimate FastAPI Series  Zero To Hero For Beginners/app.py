from fastapi import FastAPI, Query, Path, UploadFile
from typing import Optional, Annotated
from pydantic import BaseModel, Field
from models import UserIn,UserOut,BaseUser,Item,Image

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI!"}


random_list = [
{"abc" : "def"},
{"def" : "ghi"},
{"ghi" : "jkl"},
{"jkl" : "mno"}]

@app.get("/query")
def query(skip:int, limit:int):
    return random_list[skip:skip+limit]

@app.get("/queryuser")
def query_user(name:Optional[str]=None):
    res = {"user_id": "1"}
    if name is not None:
        res.update({"name": name})
    return res

@app.get("/user/{user_id}")
def get_user(user_id:int, name: Optional[str]= None):
    res = {"user_id": user_id}
    if name is not None:
        res.update({"name": name})
    return res

# client -> server (request body) can't use GET
# server -> client (response body) always
@app.post("/create_item/")
async def create_item(item:Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.get("/items")
async def get_items(q: Annotated[Optional[list[str]], Query(title="add more items",min_length=3, max_length=10)] = None):

    res = {"items": [{"item":"ball"}]}
    if q:
        res.update({"item": q})

@app.get("/item/{item_id}")
async def get_item_id(
    *,
    item_id:int =Path(gt=10,le=100),
    q:str):

    res = {"item_id": item_id, "items" :[{"item": "ball"}]}
    if q:
        for item in q:
            res["items"].append({"item":item})
    return res

@app.post("/create_item")
async def create_item(item:Item):
    return item

@app.post("/user", response_model=UserOut)
async def create_user(user: UserIn):
    return user

@app.post("/file")
async def upload_file(file : UploadFile):
    filename = file.filename
    content = await file.read()
    return {"filename": filename,
            "content": content}

