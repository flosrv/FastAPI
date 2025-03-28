from fastapi import APIRouter, FastAPI, Header, status
from fastapi.exceptions import HTTPException
from typing import Optional, List
from data.book_data import books
from models.books_models import BookModel, BookUpdateModel
import logging

logging.basicConfig(level=logging.DEBUG)
book_endpoint = APIRouter()

################# BOOK METHODS ########################################################

# GET ALL BOOKS
@book_endpoint.get('/', response_model=List[BookModel])
async def get_all_books():
    logging.debug("Fetching all books")
    return books

# GET BOOK BY ID
@book_endpoint.get('/{book_id}')
async def get_book(book_id: int):
    logging.debug(f"Fetching book with ID {book_id}")
    for book in books:
        if book["id"] == book_id:
            logging.debug(f"Book found: {book}")
            return book
    logging.error(f"Book with ID {book_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")

# POST BOOK
@book_endpoint.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book_data: BookModel):
    logging.debug(f"Creating a new book with data: {book_data}")
    new_book = book_data.model_dump()
    books.append(new_book)
    logging.info(f"New book created: {new_book}")
    return new_book

# UPDATE BOOK
@book_endpoint.patch('/{book_id}', status_code=status.HTTP_200_OK)
async def updating_partially_book(book_id: int, book_update_data: BookUpdateModel):
    logging.debug(f"Updating book with ID {book_id} with data: {book_update_data}")
    for book in books:
        if book["id"] == book_id:
            logging.debug(f"Updating fields for book ID {book_id}")
            book["title"] = book_update_data.title
            book["author"] = book_update_data.author
            book["publisher"] = book_update_data.publisher
            book["page_count"] = book_update_data.page_count
            book["language"] = book_update_data.language
            logging.info(f"Book updated: {book}")
            return book
    logging.error(f"Book with ID {book_id} not found for update")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")

# DELETE BOOK
@book_endpoint.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    logging.debug(f"Deleting book with ID {book_id}")
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            logging.info(f"Book with ID {book_id} deleted")
            return {}
    logging.error(f"Book with ID {book_id} not found for deletion")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found")


############## QUERY PARAMETERS ###########################################################

@book_endpoint.get("/get_headers", status_code=200)
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
    user_agent: str = Header(None),
    host: str = Header(None)
):
    logging.debug(f"Received headers: Accept={accept}, Content-Type={content_type}, User-Agent={user_agent}, Host={host}")
    
    request_headers = {
        "Accept": accept, 
        "Content-Type": content_type, 
        "User-Agent": user_agent, 
        "Host": host
    }
    # Log the headers for debugging purposes
    logging.info(f"Request Headers: {request_headers}")
    return request_headers
