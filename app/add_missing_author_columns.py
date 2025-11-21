
from sqlalchemy import create_engine, text
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Varun_2002@localhost:5432/gutenberg")


engine = create_engine(DATABASE_URL)

columns_to_add = {
    "birth_year": "INTEGER",
    "death_year": "INTEGER"
}

try:
    with engine.begin() as conn: 
        for column_name, column_type in columns_to_add.items():
            conn.execute(
                text(f"ALTER TABLE authors ADD COLUMN IF NOT EXISTS {column_name} {column_type};")
            )
    print("Missing author columns added successfully!")

except Exception as e:
    print("Error adding columns:", e)
