import streamlit as st
import sqlite3
import pandas as pd
import requests
from weather import get_weather

# Page Configuration
st.set_page_config(
    page_title="Aseem Farms",
    page_icon="🌾",
    layout="wide"
)

st.title("🌾 Aseem Farms Production and Information Management System")

# Sidebar Menu
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Farm Records",
        "Crop Information",
        "Weather"
    ]
)

# Home
if menu == "Home":

    st.header("Welcome")

    st.write("""
This system helps manage production records for Aseem Farms.

### Features
- Store farm records using SQLite
- Generate sample farm data
- View crop information
- View weather information
""")

# Farm Records
elif menu == "Farm Records":

    st.header("Farm Production Records")

    conn = sqlite3.connect("farm.db")

    data = pd.read_sql_query(
        "SELECT * FROM farm_records",
        conn
    )

    st.dataframe(data)


    # Export CSV
    csv = data.to_csv(index=False)

    st.download_button(
        label="📥 Download Records (CSV)",
        data=csv,
        file_name="farm_records.csv",
        mime="text/csv"
    )
    st.subheader("✏️ Update Record")

    record_id = st.number_input(
        "Record ID",
        min_value=1,
        step=1
    )

    crop = st.selectbox(
        "Crop",
        ["Maize", "French Beans", "Broccoli", "Tomatoes", "Rice"]
    )

    field = st.selectbox(
        "Field",
        ["Field A", "Field B", "Field C", "Field D", "Field E"]
    )

    planting_date = st.date_input("Planting Date")

    harvest_date = st.date_input("Harvest Date")

    quantity = st.number_input(
        "Quantity (kg)",
        min_value=0
    )

    price = st.number_input(
        "Price per kg",
        min_value=0.0
    )

    status = st.selectbox(
        "Status",
        ["Growing", "Ready", "Harvested"]
    )

    # update record
    if st.button("Update Record"):
        revenue = quantity * price

        cursor = conn.cursor()

        cursor.execute("""
            UPDATE farm_records
            SET crop = ?,
                field_name = ?,
                planting_date = ?,
                harvest_date = ?,
                quantity_kg = ?,
                price_per_kg = ?,
                revenue = ?,
                status = ?
            WHERE id = ?
        """, (
            crop,
            field,
            planting_date,
            harvest_date,
            quantity,
            price,
            revenue,
            status,
            record_id
        ))

        conn.commit()

        st.success("Record updated successfully!")
        st.experimental_rerun()

    # Delete Record
    st.subheader("🗑 Delete Record")

    delete_id = st.number_input(
        "Enter Record ID to Delete",
        min_value=1,
        step=1,
        key="delete"
    )

    if st.button("Delete Record"):
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM farm_records WHERE id = ?",
            (delete_id,)
        )

        conn.commit()

        st.success("Record deleted successfully!")
        st.experimental_rerun()

    conn.close()

# Weather
elif menu == "Weather":

    st.header("Weather Information")

    temperature, day_time, condition, wind_speed = get_weather()

    st.metric("🌡 Temperature", f"{temperature} °C")
    st.write("🕒", day_time)
    st.write("🌦 Condition:", condition)
    st.write("💨 Wind Speed:", wind_speed, "km/h")
