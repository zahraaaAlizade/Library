from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.engin import get_db
from oprations.query_opration import AuthorOpration, BookOpration
from schema._input import RegisterInput, AddNewBook, UpdateDetailBooks, DeleteBooks
from db.model import Books, Author
from typing import List

router = APIRouter()


# @router.get("/authors", tags=['Authors'])
# async def get_authors(db=Depends(get_db)):
#     authors = db.query(Author).all()
#
#     return authors


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


def get_db():
    db = AsyncSession()
    return BookOpration(db)


@router.get("/books", tags=['Get All Books'])
async def get_all_book(
        db_session: Annotated[AsyncSession, Depends(get_db)]) -> List[Books]:
    # book_operation: BookOpration = Depends(get_db)) -> List[Books]:
    return await BookOpration(db_session).get_all_books()


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
        db_session: Annotated[AsyncSession, Depends(get_db)],
        data: DeleteBooks = Body(),
):
    remove_book = await BookOpration(db_session).delete_book(
        data.book_id
    )
    return remove_book
