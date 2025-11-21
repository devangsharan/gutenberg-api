from sqlalchemy import text
from app.database import engine

with engine.connect() as conn:
    # Wrap SQL in text()
    conn.execute(
        text("ALTER TABLE books ADD COLUMN IF NOT EXISTS download_count INTEGER DEFAULT 0;")
    )
    conn.commit()

print("Column 'download_count' added successfully!")
