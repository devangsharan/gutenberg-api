from fastapi import FastAPI, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import Base, engine, get_db
from app import models, schemas, crud

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Gutenberg Books API")

def _csv_to_list(param: Optional[List[str]]) -> Optional[List[str]]:
    if not param:
        return None
    out = []
    for p in param:
        if isinstance(p, str) and "," in p:
            out.extend([x.strip() for x in p.split(",") if x.strip()])
        elif p:
            out.append(str(p).strip())
    return out or None

@app.get("/books", response_model=schemas.BookListResponse)
def read_books(
    id: Optional[List[str]] = Query(None),
    language: Optional[List[str]] = Query(None),
    mime_type: Optional[List[str]] = Query(None, alias="mime_type"),
    topic: Optional[List[str]] = Query(None),
    author: Optional[List[str]] = Query(None),
    title: Optional[List[str]] = Query(None),
    limit: int = Query(25, ge=1, le=25),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    id_list = _csv_to_list(id)
    if id_list:
        try:
            id_list = [int(x) for x in id_list]
        except:
            raise HTTPException(status_code=400, detail="id must be integer(s)")

    languages = _csv_to_list(language)
    mime_types = _csv_to_list(mime_type)
    topics = _csv_to_list(topic)
    authors = _csv_to_list(author)
    titles = _csv_to_list(title)

    total, books = crud.get_books(
        db,
        ids=id_list,
        languages=languages,
        mime_types=mime_types,
        topics=topics,
        authors=authors,
        titles=titles,
        limit=limit,
        offset=offset
    )

    next_offset = offset + limit if (offset + limit) < total else None

    books_out = []
    for b in books:
        books_out.append({
            "gutenberg_id": b.gutenberg_id,
            "title": b.title,
            "authors": [
                {
                    "id": a.id,
                    "name": a.name,
                    "birth_year": getattr(a, "birth_year", None),
                    "death_year": getattr(a, "death_year", None)
                }
                for a in b.authors
            ],
            "genre": [bs.name for bs in b.bookshelves],
            "language": b.language,
            "subjects": [s.name for s in b.subjects],
            "bookshelves": [bs.name for bs in b.bookshelves],
            "formats": [{"mime_type": f.mime_type, "url": f.url} for f in b.formats],
            "download_count": getattr(b, "download_count", getattr(b, "downloads", 0))
        })

    return {
        "total": total,
        "books": books_out
    }
