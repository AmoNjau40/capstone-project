import sqlite3

conn = sqlite3.connect("farm.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS farm_records(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop TEXT,
    field_name TEXT,
    planting_date TEXT,
    harvesting_date TEXT,
    quantity_kg REAL,
    price_per_kg REAL,
    revenue REAL,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully.")
