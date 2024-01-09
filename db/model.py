from sqlalchemy.orm import Mapped, mapped_column, relationship

from .engin import Base


class Books(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column()
    author: Mapped[str] = mapped_column()
    genre: Mapped[str] = mapped_column()
    published_date: Mapped[str] = mapped_column()
    isbn: Mapped[str] = mapped_column()
    quantity_available: Mapped[int] = mapped_column()


class Author(Base):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column()
    biography: Mapped[str] = mapped_column()
    # books: relationship("Book", backref="author")

