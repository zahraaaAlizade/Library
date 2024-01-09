from pydantic import BaseModel


class RegisterInput(BaseModel):
    author_id: int
    name: str
    biography: str


class AddNewBook(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    published_date: str
    isbn: str
    quantity_available: int


class UpdateDetailBooks(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    published_date: str


class DeleteBooks(BaseModel):
    book_id: int
