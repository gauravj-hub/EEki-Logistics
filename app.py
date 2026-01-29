import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Eeki Farms", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Data Entry - NO ERRORS!")

# Use BUILT-IN Streamlit connection (no external packages needed)
@st.cache_resource
def get_connection():
    return st.connection("gsheets")

conn = get_connection()

# Connection test
col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Test Connection", type="secondary"):
        try:
            df = conn.read()
            st.success("✅ CONNECTION WORKS!")
            st.dataframe(df.head())
        except Exception as e:
            st.error(f"❌ Connection failed: {e}")

# SIMPLIFIED FORM
st.subheader("📝 Enter Farm Data")
with st.form("farm_form"):
    col1, col2 = st.columns(2)
    with col1:
        farm1 = st.text_input("Farm 1 *")
        loc1 = st.text_input("Location 1 *")
        vendor = st.text_input("Vendor *")
    with col2:
        crop1 = st.text_input("Crop 1 *")
        qty1 = st.number_input("Quantity 1 (kg) *", min_value=0.01)
        entry_date = st.date_input("Date", value=date.today())
    
    submitted = st.form_submit_button("🚀 Save to Google Sheets")

if submitted:
    if all([farm1, loc1, vendor, crop1]):
        try:
            # Read existing data + append new row
            existing_df = conn.read()
            new_row = pd.DataFrame({
                "Farm": [farm1], "Location": [loc1], "Crop": [crop1], 
                "Quantity": [qty1], "Vendor": [vendor], "Date": [str(entry_date)]
            })
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            
            # Write back to sheet
            conn.update(data=updated_df)
            st.success("✅ DATA SAVED TO GOOGLE SHEETS!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"❌ Save error: {e}")
    else:
        st.error("Fill all required fields (*)")

# Show data
if st.checkbox("📊 View All Data"):
    try:
        df = conn.read()
        st.dataframe(df, use_container_width=True)
        st.caption(f"Total records: {len(df)}")
    except:
        st.info("No data or connection issue")
