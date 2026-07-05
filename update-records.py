import sqlite3

conn = sqlite3.connect("farm.db")
cursor = conn.cursor()

cursor.execute("""
UPDATE farm_records
SET status = ?
WHERE id = ?
""", ("Harvested", 1))

conn.commit()
conn.close()

print("Record updated successfully!")