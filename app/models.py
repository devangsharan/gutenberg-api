from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base



book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

book_subjects = Table(
    "book_subjects",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("subject_id", ForeignKey("subjects.id"), primary_key=True),
)

book_bookshelves = Table(
    "book_bookshelves",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("bookshelf_id", ForeignKey("bookshelves.id"), primary_key=True),
)

book_formats = Table(
    "book_formats",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("format_id", ForeignKey("formats.id"), primary_key=True),
)



class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    gutenberg_id = Column(Integer, unique=True, index=True)
    title = Column(String)
    language = Column(String)
    download_count = Column(Integer, default=0)

    authors = relationship("Author", secondary=book_authors, back_populates="books")
    subjects = relationship("Subject", secondary=book_subjects, back_populates="books")
    bookshelves = relationship("Bookshelf", secondary=book_bookshelves, back_populates="books")
    formats = relationship("Format", secondary=book_formats, back_populates="books")


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    birth_year = Column(Integer, nullable=True)
    death_year = Column(Integer, nullable=True)

    books = relationship("Book", secondary=book_authors, back_populates="authors")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship("Book", secondary=book_subjects, back_populates="subjects")


class Bookshelf(Base):
    __tablename__ = "bookshelves"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship("Book", secondary=book_bookshelves, back_populates="bookshelves")


class Format(Base):
    __tablename__ = "formats"

    id = Column(Integer, primary_key=True)
    mime_type = Column(String)
    url = Column(String)

    books = relationship("Book", secondary=book_formats, back_populates="formats")
