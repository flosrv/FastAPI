from fastapi import APIRouter, FastAPI, Header,status, HTTPException
from typing import Optional, List
from data.book_data import books
from models.books_models import BookModel, BookUpdateModel
import logging

logging.basicConfig(level=logging.DEBUG)
endPoints = APIRouter()
app = FastAPI()

################# BOOK METHODS ########################################################

# GET ALL BOOKS

@app.get('/books', response_model=List[BookModel])
async def get_all_books():
    return books

# GET BOOK BY ID

@app.get('/book/{book_id}')
async def get_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Book not Found")
# POST BOOK

@app.post('/create_book', status_code=status.HTTP_201_CREATED)
async def create_book(book_data:BookModel):
    new_book  = book_data.model_dump()
    books.append(new_book)
    return new_book

# UPDATE BOOK

@app.patch('/book/{book_id}', status_code=status.HTTP_200_OK)
async def updating_partially_book(book_id:int, book_update_data:BookUpdateModel):
    for book in books:
        if book["id"] == book_id:
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Book not Found")

# DELETE BOOK

@app.delete('/book/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id:int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail="Book not Found")


############## QUERY PARAMETERS ###########################################################

#
@app.get("/get_headers", status_code=200 )
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
    ):

    request_headers = {
        "Accept": accept, 
        "Content-Type": content_type, 
        "User-Agent":  user_agent, 
        "Host": host}
    # Log the headers for debugging purposes
    logging.info(f"Request Headers: {request_headers}")
    return request_headers
