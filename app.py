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
        "Dashboard",
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
# dashboard
elif menu == "Dashboard":

    st.header("📊 Dashboard")

    conn = sqlite3.connect("farm.db")

    data = pd.read_sql_query("SELECT * FROM farm_records", conn)

    conn.close()

    if data.empty:
        st.warning("No farm records available.")
    else:

        # Total Production
        total_production = data["quantity_kg"].sum()

        # Total Revenue
        if "price_per_kg" in data.columns:
            total_revenue = (
                data["quantity_kg"] * data["price_per_kg"]
            ).sum()
        else:
            total_revenue = 0

        # Number of Crop Types
        total_crops = data["crop"].nunique()

        # Harvested Crops
        harvested = len(
            data[data["status"] == "Harvested"]
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🌾 Total Production",
                f"{total_production:,.0f} kg"
            )

            st.metric(
                "🌱 Crop Types",
                total_crops
            )

        with col2:
            st.metric(
                "💰 Total Revenue",
                f"KES {total_revenue:,.2f}"
            )

            st.metric(
                "✅ Harvested Crops",
                harvested
            )
# farm records
elif menu == "Farm records":

    st.header("Farm Production Records")

    conn = sqlite3.connect("farm.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS farm_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crop TEXT,
            field_name TEXT,
            planting_date TEXT,
            quantity_kg REAL,
            price_per_kg REAL,
            revenue REAL,
            status TEXT
        )
        """
    )

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

    

    st.subheader("➕ Add Record")

    with st.form("add_record"):
        add_crop = st.selectbox(
            "Crop",
            ["Maize", "Tomatoes", "French Beans", "Broccoli", "Rice"],
            key="add_crop"
        )

        add_field = st.selectbox(
            "Field",
            ["Field A", "Field B", "Field C", "Field D", "Field E"],
            key="add_field"
        )

        add_planting_date = st.date_input(
            "Planting Date",
            key="add_date"
        )

        add_quantity = st.number_input(
            "Quantity (kg)",
            min_value=0.0,
            step=1.0,
            key="add_quantity"
        )

        add_price = st.number_input(
            "Price per kg",
            min_value=0.0,
            key="add_price"
        )

        add_status = st.selectbox(
            "Status",
            ["Growing", "Ready", "Harvested"],
            key="add_status"
        )

        submitted = st.form_submit_button("Add Record")

        if submitted:
            revenue = add_quantity * add_price

            cursor.execute(
                """
                INSERT INTO farm_records
                (crop, field_name, planting_date, quantity_kg,
                 price_per_kg, revenue, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    add_crop,
                    add_field,
                    str(add_planting_date),
                    add_quantity,
                    add_price,
                    revenue,
                    add_status
                )
            )

            conn.commit()

            st.success("Record added successfully!")
            st.rerun()

    st.subheader("✏️ Update Record")

    record_id = st.number_input(
        "Record ID",
        min_value=1,
        step=1,
        key="update_id"
    )

    update_crop = st.selectbox(
        "Crop",
        ["Maize", "French Beans", "Broccoli", "Tomatoes", "Rice"],
        key="update_crop"
    )

    update_field = st.selectbox(
        "Field",
        ["Field A", "Field B", "Field C", "Field D", "Field E"],
        key="update_field"
    )

    update_planting_date = st.date_input(
        "Planting Date",
        key="update_date"
    )

    update_quantity = st.number_input(
        "Quantity (kg)",
        min_value=0,
        key="update_quantity"
    )

    update_price = st.number_input(
        "Price per kg",
        min_value=0.0,
        key="update_price"
    )

    update_status = st.selectbox(
        "Status",
        ["Growing", "Ready", "Harvested"],
        key="update_status"
    )
    if st.button("Update Record"):
        revenue = update_quantity * update_price

        cursor.execute(
            """
            UPDATE farm_records
            SET crop = ?,
                field_name = ?,
                planting_date = ?,
                quantity_kg = ?,
                price_per_kg = ?,
                revenue = ?,
                status = ?
            WHERE id = ?
            """,
            (
                update_crop,
                update_field,
                str(update_planting_date),
                update_quantity,
                update_price,
                revenue,
                update_status,
                record_id
            )
        )

        conn.commit()

        st.success("Record updated successfully!")
        st.rerun()
    # Delete record
    st.subheader("🗑 Delete Record")

    delete_id = st.number_input(
        "Enter Record ID to Delete",
        min_value=1,
        step=1,
        key="delete"
    )

    if st.button("Delete Record"):
        cursor.execute(
            "DELETE FROM farm_records WHERE id = ?",
            (delete_id,)
        )

        conn.commit()

        st.success("Record deleted successfully!")
        st.rerun()

    conn.close()

# Crop Information
elif menu == "Crop Information":

    crop_data = pd.read_csv("crop_information.csv")

    st.subheader("🌱 Crop Information")

    selected_crop = st.selectbox("Choose a crop", crop_data["Crop"])

    crop = crop_data[crop_data["Crop"] == selected_crop].iloc[0]

    st.write(f"### {crop['Crop']}")
    st.write(crop["Description"])

# Weather
elif menu == "Weather":

    st.header("Weather Information")

    temperature, day_time, condition, wind_speed = get_weather()

    st.metric("🌡 Temperature", f"{temperature} °C")
    st.write("🕒", day_time)
    st.write("🌦 Condition:", condition)
    st.write("💨 Wind Speed:", wind_speed, "km/h")
