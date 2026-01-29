import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Eeki Farms", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Data Entry")

# Use correct connection type
@st.cache_resource
def get_connection():
    return st.connection("gsheets", type=st.gsheets.GSheetsConnection)

try:
    conn = get_connection()
    st.success("✅ Connected!")
except:
    st.error("❌ Connection failed - check secrets.toml")
    st.stop()

# Test buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Test Read"):
        try:
            df = conn.read(worksheet="Sheet1")
            st.success("✅ READ OK!")
            st.dataframe(df.tail(3))
        except Exception as e:
            st.error(f"Read error: {e}")

with col2:
    if st.button("🧪 Test Write"):
        try:
            test_row = pd.DataFrame({"Test": ["Write Test"], "Date": [str(date.today())]})
            existing = conn.read(worksheet="Sheet1")
            new_data = pd.concat([existing, test_row])
            conn.update(worksheet="Sheet1", data=new_data)
            st.success("✅ WRITE OK!")
        except Exception as e:
            st.error(f"Write error: {e}")

# MAIN FORM
st.subheader("📝 Farm Data Entry")
with st.form("farm_data"):
    col1, col2 = st.columns(2)
    with col1:
        farm1 = st.text_input("Farm 1 *")
        loc1 = st.text_input("Location 1 *")
        vendor = st.text_input("Vendor *")
    with col2:
        crop1 = st.text_input("Crop 1 *")
        qty1 = st.number_input("Quantity (kg) *", min_value=0.01)
        date_entry = st.date_input("Date")
    
    submit = st.form_submit_button("🚀 Save", type="primary")
    
    if submit and all([farm1, loc1, vendor, crop1]):
        try:
            new_row = pd.DataFrame({
                "Farm": [farm1], "Location1": [loc1], "Crop1": [crop1],
                "Quantity1": [qty1], "Vendor": [vendor], "Date": [str(date_entry)]
            })
            existing = conn.read(worksheet="Sheet1")
            updated = pd.concat([existing, new_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated)
            st.success("✅ SAVED!")
            st.balloons()
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")

if st.checkbox("📊 Show Data"):
    df = conn.read(worksheet="Sheet1")
    st.dataframe(df)
