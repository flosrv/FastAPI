
from fastapi import FastAPI, Header,status, HTTPException

from typing import Optional, List
import logging
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "publisher": "Charles Scribner's Sons",
        "publisher_date": "1925-04-10",
        "page_count": 218,
        "language": "English"
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "publisher": "J.B. Lippincott & Co.",
        "publisher_date": "1960-07-11",
        "page_count": 281,
        "language": "English"
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "publisher": "Secker & Warburg",
        "publisher_date": "1949-06-08",
        "page_count": 328,
        "language": "English"
    },
    {
        "id": 4,
        "title": "Les Misérables",
        "author": "Victor Hugo",
        "publisher": "A. Lacroix, Verboeckhoven & Cie",
        "publisher_date": "1862-04-03",
        "page_count": 1463,
        "language": "French"
    },
    {
        "id": 5,
        "title": "Don Quixote",
        "author": "Miguel de Cervantes",
        "publisher": "Francisco de Robles",
        "publisher_date": "1605-01-16",
        "page_count": 863,
        "language": "Spanish"
    },
    {
        "id": 6,
        "title": "One Hundred Years of Solitude",
        "author": "Gabriel García Márquez",
        "publisher": "Editorial Sudamericana",
        "publisher_date": "1967-05-30",
        "page_count": 417,
        "language": "Spanish"
    },
    {
        "id": 7,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "publisher": "Little, Brown and Company",
        "publisher_date": "1951-07-16",
        "page_count": 277,
        "language": "English"
    },
    {
        "id": 8,
        "title": "Crime and Punishment",
        "author": "Fyodor Dostoevsky",
        "publisher": "The Russian Messenger",
        "publisher_date": "1866-01-01",
        "page_count": 671,
        "language": "Russian"
    },
    {
        "id": 9,
        "title": "Pride and Prejudice",
        "author": "Jane Austen",
        "publisher": "T. Egerton, Whitehall",
        "publisher_date": "1813-01-28",
        "page_count": 432,
        "language": "English"
    },
    {
        "id": 10,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "publisher": "HarperCollins",
        "publisher_date": "1988-04-01",
        "page_count": 208,
        "language": "Portuguese"
    }
]

logging.basicConfig(level=logging.INFO)


class BookModel(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    publisher_date: str
    page_count: int
    language: str
 

class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str

@app.get("/")
async def root():
    try:
        return {"message": "Hello World"}
    except Exception as e:
        logging.error(e)
        return {"message": "Error"}

@app.get('/greet/')
async def greet_name(age:int = 0, name: Optional[str] = "User"):
    return {'message': f'Hello, {name}', "age":age}


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



############ POST METHODS ####################################################################

