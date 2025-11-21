import requests
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Author, Subject, Bookshelf, Format, Book
from app.utils import clean_url, extract_language

DATA_URL = "https://gutendex.com/books/?page="

Base.metadata.create_all(bind=engine)

def fetch_all_books():
    page = 1
    results = []

    while True:
        url = f"{DATA_URL}{page}"
        r = requests.get(url)

        if r.status_code != 200:
            break

        data = r.json()
        results.extend(data["results"])

        if not data["next"]:
            break

        page += 1

    return results


def seed_database():
    db: Session = SessionLocal()

    books_data = fetch_all_books()

    for item in books_data:
        gutenberg_id = item["id"]

        exists = db.query(Book).filter(Book.gutenberg_id == gutenberg_id).first()
        if exists:
            continue

        book = Book(
            gutenberg_id=gutenberg_id,
            title=item.get("title", ""),
            language=extract_language(item.get("languages")),
            download_count=item.get("download_count", 0)
        )

        for a in item.get("authors", []):
            author = db.query(Author).filter(Author.name == a["name"]).first()
            if not author:
                author = Author(
                    name=a["name"],
                    birth_year=a.get("birth_year"),
                    death_year=a.get("death_year")
                )
                db.add(author)
            book.authors.append(author)

        for s in item.get("subjects", []):
            subj = db.query(Subject).filter(Subject.name == s).first()
            if not subj:
                subj = Subject(name=s)
                db.add(subj)
            book.subjects.append(subj)

        for bs in item.get("bookshelves", []):
            shelf = db.query(Bookshelf).filter(Bookshelf.name == bs).first()
            if not shelf:
                shelf = Bookshelf(name=bs)
                db.add(shelf)
            book.bookshelves.append(shelf)

        for mime, url in item.get("formats", {}).items():
            fmt = Format(
                mime_type=mime,
                url=clean_url(url)
            )
            db.add(fmt)
            book.formats.append(fmt)

        db.add(book)
        db.commit()

    db.close()


if __name__ == "__main__":
    seed_database()
