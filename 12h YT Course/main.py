
from fastapi import FastAPI, Header,status, HTTPException
from models import books_models
from routes.routes import endPoints
from typing import Optional, List
import logging

app = FastAPI()


logging.basicConfig(level=logging.INFO)



@app.get("/")
async def root():
    try:
        return {"message": "Hello World"}
    except Exception as e:
        logging.error(e)
        return {"message": "Error"}
