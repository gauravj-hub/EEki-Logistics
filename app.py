import streamlit as st
import pandas as pd
from datetime import date
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Eeki Farms Data Entry", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Customer Data Entry")

# Test connection first
@st.cache_resource
def init_connection():
    return st.connection("gsheets", type=GSheetsConnection)

conn = init_connection()

# Show connection status
if conn:
    try:
        test_data = conn.read(worksheet="Sheet1", nrows=1)
        st.success("✅ Connected to Google Sheets!")
    except:
        st.error("❌ Cannot access Sheet1 - check sharing/settings")
else:
    st.stop()

# Form (same layout)
col1, col2 = st.columns(2)
with col1:
    st.subheader("Farms & Locations")
    farm1 = st.text_input("Farm 1", placeholder="Enter Farm 1 name")
    farm2 = st.text_input("Farm 2")
    farm3 = st.text_input("Farm 3")
    farm4 = st.text_input("Farm 4")
    farm5 = st.text_input("Farm 5")
    loc1 = st.text_input("Location 1")
    loc2 = st.text_input("Location 2")

with col2:
    st.subheader("Crops & Quantities")
    crop1 = st.text_input("Crop 1")
    qty1 = st.number_input("Quantity Crop 1 (kg)", min_value=0.0, format="%.2f")
    crop2 = st.text_input("Crop 2")
    qty2 = st.number_input("Quantity Crop 2 (kg)", min_value=0.0, format="%.2f")

col3, col4, col5 = st.columns(3)
vendor = col3.text_input("Vendor")
transport_cost = col4.number_input("Transportation Cost (₹)", min_value=0.0, format="%.2f")
running_km = col5.number_input("Running Km", min_value=0, step=1)

entry_date = st.date_input("Date", value=date.today())

if st.button("🚀 Submit to Google Sheets", type="primary"):
    if farm1 and loc1 and crop1 and vendor and qty1 > 0:
        new_row = {
            "Farm": farm1, "Farm2": farm2, "Farm3": farm3, "Farm4": farm4, "Farm5": farm5,
            "Location1": loc1, "Location2": loc2, "Crop1": crop1, "Quantity1": qty1,
            "Crop2": crop2, "Quantity2": qty2, "Vendor": vendor, 
            "Transportation_Cost": transport_cost, "Running_Km": running_km, "Date": str(entry_date)
        }
        
        try:
            # ✅ CORRECT WAY: Read existing + append new row
            existing_data = conn.read(worksheet="Sheet1")
            new_df = pd.DataFrame([new_row])
            updated_data = pd.concat([existing_data, new_df], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_data)
            
            st.success("✅ NEW ROW ADDED TO GOOGLE SHEETS!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Save failed: {str(e)}")
    else:
        st.error("⚠️ Fill: Farm1, Location1, Crop1+Qty, Vendor")

# Always show recent data
if st.checkbox("📊 Show All Data", value=True):
    try:
        df = conn.read(worksheet="Sheet1")
        st.dataframe(df, use_container_width=True)
        st.caption(f"Total entries: {len(df)}")
    except:
        st.warning("Cannot display data")
