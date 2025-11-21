from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func, select, desc, literal_column
from . import models

DOWNLOAD_FIELDS = ("downloads", "download_count", "downloaded", "num_downloads")

def _choose_download_col():
    for f in DOWNLOAD_FIELDS:
        if hasattr(models.Book, f):
            return getattr(models.Book, f)
    return models.Book.id

DOWNLOAD_COL = _choose_download_col()

def _apply_topic_filter(q, topics):
    conds = []
    for t in topics:
        conds.append(models.Subject.name.ilike(f"%{t}%"))
        conds.append(models.Bookshelf.name.ilike(f"%{t}%"))
    q = q.outerjoin(models.Book.subjects).outerjoin(models.Book.bookshelves)
    return q.filter(or_(*conds))

def _apply_mime_filter(q, mime_types):
    conds = [models.Format.mime_type.ilike(f"%{m}%") for m in mime_types]
    q = q.join(models.Book.formats)
    return q.filter(or_(*conds))

def get_books(db: Session,
              ids=None,
              languages=None,
              mime_types=None,
              topics=None,
              authors=None,
              titles=None,
              limit: int = 25,
              offset: int = 0):
    if limit is None or limit <= 0:
        limit = 25
    if limit > 25:
        limit = 25
    q = db.query(models.Book).options(
        joinedload(models.Book.authors),
        joinedload(models.Book.subjects),
        joinedload(models.Book.bookshelves),
        joinedload(models.Book.formats)
    )

    if ids:
        q = q.filter(models.Book.gutenberg_id.in_(ids))
    if languages:
        q = q.filter(models.Book.language.in_(languages))
    if titles:
        title_conds = [models.Book.title.ilike(f"%{t}%") for t in titles]
        q = q.filter(or_(*title_conds))
    if authors:
        q = q.join(models.Book.authors).filter(or_(*[models.Author.name.ilike(f"%{a}%") for a in authors]))
    if topics:
        q = _apply_topic_filter(q, topics)
    if mime_types:
        q = _apply_mime_filter(q, mime_types)

    subq = q.with_entities(models.Book.id).distinct().subquery()
    total = db.query(func.count()).select_from(subq).scalar()

    q = q.order_by(desc(DOWNLOAD_COL), models.Book.gutenberg_id.desc()).distinct().offset(offset).limit(limit)
    books = q.all()

    return total or 0, books
