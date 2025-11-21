Project Gutenberg API

This repository contains a FastAPI implementation of an API to query and access books from Project Gutenberg. The API supports filtering by language, author, title, topic, and MIME type, and returns paginated results in JSON format.

Table of Contents

Features

Project Structure

Prerequisites

Setup Instructions

Running the API

Example API Calls

Adding Data

.gitignore

Contributing

Features

Retrieve books with filters:

Book IDs (Project Gutenberg IDs)

Language

Author (supports partial and case-insensitive search)

Title (supports partial and case-insensitive search)

Topic (matches subject or bookshelf, case-insensitive partial match)

MIME type

Pagination support (25 books per page)

Returns books sorted by download count (popularity)

JSON response containing:

Book title

Author information

Language

Subject(s)

Bookshelf(s)

Available formats and download links

Project Structure

The folder structure for this project is:

gutenberg-api/ (root folder)

app/

__init__.py – marks the folder as a Python package

main.py – the FastAPI app

models.py – SQLAlchemy models for books, authors, subjects, bookshelves, and formats

schemas.py – Pydantic schemas for validating API responses

database.py – database connection setup

add_dummy_books.py – script to add dummy books, authors, and related data

add_missing_author_columns.py – script to update missing columns in authors table

requirements.txt – Python dependencies

.gitignore – ignores unnecessary files for git

README.md – this file

venv/ – Python virtual environment

Prerequisites

Before running this project, you need:

Python 3.10+

PostgreSQL or MySQL database

pip or pipenv for installing Python packages

uvicorn for running FastAPI

Optional: VS Code or any preferred IDE

Setup Instructions

Clone the repository
Open terminal or PowerShell and run:
git clone https://github.com/<your-username>/gutenberg-api.git
cd gutenberg-api

Create a virtual environment
On Windows:
python -m venv venv
venv\Scripts\activate

On Mac/Linux:
python -m venv venv
source venv/bin/activate

Install dependencies
Run:
pip install -r requirements.txt

Configure the database

Create a PostgreSQL or MySQL database.

Update the database URL in app/database.py:

For PostgreSQL:
DATABASE_URL = "postgresql://username:password@localhost:5432/gutenberg"

For MySQL:
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/gutenberg"

Add missing author columns
Run the script to ensure all author columns exist:
python -m app.add_missing_author_columns

Add dummy data (optional)
If you want some test data in the database, run:
python -m app.add_dummy_books

Running the API

To start the API server, run:
uvicorn app.main:app --reload

The API will be available at: http://127.0.0.1:8000

Swagger docs for testing endpoints: http://127.0.0.1:8000/docs

Example API Calls

Get all books (first 25 results)
GET /books?page=1&limit=25

Filter by language and topic
GET /books?language=en&topic=children

Search by author or title (partial match)
GET /books?author=shakespeare&title=hamlet

Multiple filters in one request
GET /books?language=en,fr&author=austen&topic=fiction

Adding Data

You can populate some dummy data for testing using add_dummy_books.py.

For real Project Gutenberg data, import the SQL dump into your database and run the API.

.gitignore

Use the following .gitignore to ignore unnecessary files:

__pycache__/
*.py[cod]
*$py.class
venv/
.env
*.log
*.sql
*.sqlite3
.DS_Store
.vscode/
.idea/
