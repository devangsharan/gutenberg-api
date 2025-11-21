# app/add_author_columns.py

from sqlalchemy import text
from app.database import engine

with engine.connect() as conn:
    conn.execute(text("ALTER TABLE authors ADD COLUMN IF NOT EXISTS birth_year INTEGER;"))
    conn.execute(text("ALTER TABLE authors ADD COLUMN IF NOT EXISTS death_year INTEGER;"))

print("Columns 'birth_year' and 'death_year' added successfully!")
