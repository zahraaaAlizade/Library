from pydantic import BaseModel


class RegisterInput(BaseModel):
    name: str
    biography: str


class AddNewBook(BaseModel):
    title: str
    author: str
    genre: str
    published_date: str
    isbn: str


class UpdateDetailBooks(BaseModel):
    book_id: int
    title: str
    author: str
    genre: str
    published_date: str


class DeleteBooks(BaseModel):
    book_id: int
