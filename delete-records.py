import sqlite3

conn = sqlite3.connect("farm.db")
cursor = conn.cursor()

cursor.execute("""
DELETE FROM farm_records
WHERE id = ?
""", (1,))

conn.commit()
conn.close()

print("Record deleted successfully!")