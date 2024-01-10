import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from db.model import Books, Author
from exeptions import AuthorNotFound, BooksNotFound, DeleteSuccessful
from typing import List, Optional


class AuthorOpration:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create(self, author_id: int, name: str, biography: str):
        new_author = Author(author_id=author_id, name=name, biography=biography)

        async with self.db_session as session:
            session.add(new_author)
            await session.commit()
        return new_author

    async def get_all_author(self):
        async with self.db_session as session:
            authors = await session.execute(sa.select(Author))
        return authors.scalars().all()

    async def get_author_by_id(self, author_id: int):
        query = sa.select(Author).where(Author.author_id == author_id)
        async with self.db_session as session:
            author_data = await session.scalar(
                query
            )
            if author_data is None:
                raise AuthorNotFound("/get")

            return author_data


class BookOpration:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def create_book(self, book_id: int, title: str, author: str, genre: str, published_date: str, isbn: str,
                          quantity_available: int):
        new_book = Books(book_id=book_id, title=title, author=author, genre=genre, published_date=published_date,
                         isbn=isbn, quantity_available=quantity_available)

        async with self.db_session as session:
            session.add(new_book)
            await session.commit()
        return new_book

    async def get_all_books(self) -> List[Books]:
        async with self.db_session as session:
            books_list = await session.execute(sa.select(Books))
        return books_list.scalars().all()

    async def get_book_by_id(self, book_id: int):
        query = sa.select(Books).where(Books.book_id == book_id)
        async with self.db_session as session:
            book_data = await session.scalar(
                query
            )
            if book_data is None:
                raise BooksNotFound("/get")

            return book_data

    async def update_book(self, book_id: int, title: str, author: str, genre: Optional[str],
                          published_date: Optional[str]):
        query_set = sa.select(Books).where(Books.book_id == book_id)
        update_books = sa.update(Books).where(Books.book_id == book_id)
        if title:
            update_books = update_books.values(title=title)
        if author:
            update_books = update_books.values(author=author)
        if genre:
            update_books = update_books.values(genre=genre)
        if published_date:
            update_books = update_books.values(published_date=published_date)

        async with self.db_session as session:
            books_data = await session.scalar(query_set)
            if books_data is None:
                raise BooksNotFound("/update")

            await session.execute(update_books)
            await session.commit()
            books_data.book_id = book_id
            return books_data

    async def delete_book(self, book_id: int):
        query_set = sa.select(Books).where(Books.book_id == book_id)
        delete_query = sa.delete(Books).where(
            Books.book_id == book_id
        )

        async with self.db_session as session:
            books_data = await session.scalar(query_set)
            if books_data is None:
                raise DeleteSuccessful("/delete")

            await session.execute(delete_query)
            await session.commit()

    async def get_books_by_genre(self, genre: str) -> List[Books]:
        async with self.db_session as session:
            query = sa.select(Books).where(Books.genre == genre)
            books_list = await session.execute(query)
        return books_list.scalars().all()

    async def get_books_by_author(self, author: str) -> List[Books]:
        async with self.db_session as session:
            query = sa.select(Books).where(Books.author == author)
            books_list = await session.execute(query)
        return books_list.scalars().all()

    async def get_books_sorted_by_published_date(self) -> List[Books]:
        async with self.db_session as session:
            query = sa.select(Books).order_by(desc(Books.published_date))
            books_list = await session.execute(query)
        return books_list.scalars().all()
