import sqlite3
import random
from datetime import datetime, timedelta
import random
from datetime import datetime, timedelta

def generate_record(crop, field):

    quantity = random.randint(500, 5000)
    price = random.randint(40, 120)
    revenue = quantity * price

    status = random.choice([
        "Growing",
        "Ready",
        "Harvested"
    ])

    planting_date = datetime.now() - timedelta(days=random.randint(30, 180))

    harvest_date = planting_date + timedelta(days=random.randint(60, 120))

    return (
        crop,
        field,
        planting_date.date(),
        harvest_date.date(),
        quantity,
        price,
        revenue,
        status
    )

#creating the crop and field names
farm_crops = [
    ("Maize", "Field A"),
    ("French Beans", "Field B"),
    ("Broccoli", "Field C"),
    ("Tomatoes", "Field D"),
    ("Rice", "Field E")
]

#connect to SQL database
conn = sqlite3.connect("farm.db")
cursor = conn.cursor()


#Insert the record into the database
for crop, field in farm_crops:

    for i in range(4):

        record = generate_record(crop, field)

        cursor.execute("""
        INSERT INTO farm_records(
            crop,
            field_name,
            planting_date,
            harvest_date,
            quantity_kg,
            price_per_kg,
            revenue,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, record)

#save changes and close
conn.commit()
conn.close()
print("record inserted successfully!")