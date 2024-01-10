from typing import Annotated, Optional
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.engin import get_db
from oprations.query_opration import AuthorOpration, BookOpration
from schema._input import RegisterInput, AddNewBook, UpdateDetailBooks

router = APIRouter()


@router.get("/authors", tags=['All Author'])
async def get_all_authors(
        db_session: Annotated[AsyncSession, Depends(get_db)]
):
    all_authors = await AuthorOpration(db_session).get_all_author()
    return all_authors


@router.post("/authors", tags=['Add Authors'])
async def add_authors(
        db_session: Annotated[AsyncSession, Depends(get_db)], data: RegisterInput = Body()
):
    author = await AuthorOpration(db_session).create(
        author_id=data.author_id, name=data.name, biography=data.biography
    )
    return author


@router.get("/authors/{author_id}", tags=['Authors'])
async def get_author_profile(
        db_session: Annotated[AsyncSession, Depends(get_db)], author_id: int
):
    author_detail = await AuthorOpration(db_session).get_author_by_id(author_id)

    return author_detail


@router.post("/books", tags=['Add New Books'])
async def add_new_book(
        db_session: Annotated[AsyncSession, Depends(get_db)], data: AddNewBook = Body()
):
    new_book = await BookOpration(db_session).create_book(
        book_id=data.book_id, title=data.title, author=data.author, genre=data.genre,
        published_date=data.published_date, isbn=data.isbn, quantity_available=data.quantity_available
    )
    return new_book


@router.get("/books/{book_id}", tags=['Get Books By ID'])
async def get_specific_book_by_id(
        db_session: Annotated[AsyncSession, Depends(get_db)], book_id: int
):
    book_detail = await BookOpration(db_session).get_book_by_id(book_id)

    return book_detail


@router.get("/books", tags=['Get All Books'])
async def get_all_book(
        db_session: Annotated[AsyncSession, Depends(get_db)]
):
    all_books = await BookOpration(db_session).get_all_books()
    return all_books


@router.put("/books/{book_id}", tags=['Update Books'])
async def book_update_detail(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        data: UpdateDetailBooks = Body(),
):
    update_book = await BookOpration(db_session).update_book(
        data.book_id, data.title, data.author, data.genre, data.published_date
    )
    return update_book


@router.delete("/books/{book_id}", tags=['Delete Books'])
async def delete_book(
        db_session: Annotated[AsyncSession, Depends(get_db)], book_id: int

):
    remove_book = await BookOpration(db_session).delete_book(
        book_id
    )
    return remove_book


@router.get("/books/filter/sort", tags=['Filter and Sort All Books'])
async def get_book_sort_and_filter(
        db_session: Annotated[AsyncSession, Depends(get_db)],
        genre: Optional[str] = None,
        author: Optional[str] = None,
        sort_by_published_date: Optional[str] = None,
):
    books_operation = BookOpration(db_session)

    if sort_by_published_date:
        sorted_books = await books_operation.get_books_sorted_by_published_date()
    elif genre:
        filtered_books = await books_operation.get_books_by_genre(genre)
    elif author:
        filtered_books = await books_operation.get_books_by_author(author)
    else:
        filtered_books = await books_operation.get_all_books()

    return sorted_books if sort_by_published_date else filtered_books
