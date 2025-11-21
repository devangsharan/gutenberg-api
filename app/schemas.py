from pydantic import BaseModel
from typing import List

class AuthorSchema(BaseModel):
    id: int
    name: str | None = None
    birth_year: int | None = None
    death_year: int | None = None

    class Config:
        orm_mode = True


class SubjectSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BookshelfSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class FormatSchema(BaseModel):
    id: int
    mime_type: str
    url: str

    class Config:
        orm_mode = True


class BookSchema(BaseModel):
    id: int
    gutenberg_id: int
    title: str
    language: str | None = None
    download_count: int

    authors: List[AuthorSchema] = []
    subjects: List[SubjectSchema] = []
    bookshelves: List[BookshelfSchema] = []
    formats: List[FormatSchema] = []

    class Config:
        orm_mode = True


class BookListResponse(BaseModel):
    total: int
    books: List[BookSchema]
