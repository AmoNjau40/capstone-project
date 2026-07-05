import sqlite3

# Connect to the database
conn = sqlite3.connect("farm.db")
cursor = conn.cursor()

# Read all records
cursor.execute("SELECT * FROM farm_records")

# Store the results
records = cursor.fetchall()

# Display each record
for record in records:
    print(record)

conn.close()