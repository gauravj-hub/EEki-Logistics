import streamlit as st
from streamlit_gsheets import GSheetsConnection as gsheets_connection  # Fixed
import pandas as pd

# Your connection code
conn = st.connection("gsheets", type=gsheets_connection)


st.set_page_config(page_title="Eeki Farms", layout="wide", page_icon="🌱")
st.title("🌱 Eeki Farms Customer Data Entry")

# CORRECT connection for service account
@st.cache_resource
def get_gsheets():
    return st.connection("gsheets", type=gsheets_connection.GSheetsConnection)

try:
    conn = get_gsheets()
    st.success("✅ Connected to Google Sheets!")
except Exception as e:
    st.error(f"❌ Connection failed: {e}")
    st.stop()

# TEST BUTTONS FIRST
col1, col2 = st.columns(2)
with col1:
    if st.button("🧪 Test Read", type="secondary"):
        try:
            df = conn.read(worksheet="Sheet1", nrows=5)
            st.success("✅ CAN READ DATA!")
            st.dataframe(df)
        except Exception as e:
            st.error(f"Read error: {e}")

with col2:
    if st.button("🧪 Test Append", type="secondary"):
        try:
            # Add test row
            test_row = pd.DataFrame([{
                "Test": "Success", "Date": str(date.today()), "Status": "Working"
            }])
            existing = conn.read(worksheet="Sheet1")
            new_data = pd.concat([existing, test_row], ignore_index=True)
            conn.update(worksheet="Sheet1", data=new_data)
            st.success("✅ CAN WRITE DATA!")
        except Exception as e:
            st.error(f"Write error: {e}")

# MAIN FORM - Your original fields
st.subheader("📝 Customer Data Entry")
with st.form("farm_form"):
    col1, col2 = st.columns([1.2, 1])
    
    with col1:
        st.subheader("Farms & Locations")
        farm1 = st.text_input("Farm 1 *")
        farm2 = st.text_input("Farm 2")
        farm3 = st.text_input("Farm 3")
        farm4 = st.text_input("Farm 4")
        farm5 = st.text_input("Farm 5")
        loc1 = st.text_input("Location 1 *")
        loc2 = st.text_input("Location 2")
    
    with col2:
        st.subheader("Crops")
        crop1 = st.text_input("Crop 1 *")
        qty1 = st.number_input("Quantity Crop 1 (kg) *", min_value=0.01, format="%.2f")
        crop2 = st.text_input("Crop 2")
        qty2 = st.number_input("Quantity Crop 2 (kg)", min_value=0.0, format="%.2f")
        
        st.subheader("Logistics")
        vendor = st.text_input("Vendor *")
        transport_cost = st.number_input("Transportation Cost (₹)", min_value=0.0)
        running_km = st.number_input("Running Km", min_value=0)
        entry_date = st.date_input("Date", value=date.today())
    
    submit = st.form_submit_button("🚀 Submit to Google Sheets", type="primary")
    
    if submit:
        required_fields = [farm1, loc1, crop1, vendor]
        if all(required_fields) and qty1 > 0:
            new_row = {
                "Farm": farm1, "Farm2": farm2, "Farm3": farm3, "Farm4": farm4, "Farm5": farm5,
                "Location1": loc1, "Location2": loc2,
                "Crop1": crop1, "Quantity1": qty1, "Crop2": crop2, "Quantity2": qty2,
                "Vendor": vendor, "Transportation_Cost": transport_cost, 
                "Running_Km": running_km, "Date": str(entry_date)
            }
            
            try:
                # Read + append + write back
                existing = conn.read(worksheet="Sheet1")
                new_df = pd.DataFrame([new_row])
                updated_data = pd.concat([existing, new_df], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_data)
                
                st.success("✅ DATA SAVED TO GOOGLE SHEETS!")
                st.balloons()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Save failed: {str(e)}")
        else:
            st.error("⚠️ Fill all * fields")

# Show all data
if st.checkbox("📊 View All Entries", value=True):
    try:
        df = conn.read(worksheet="Sheet1")
        st.dataframe(df, use_container_width=True)
        st.caption(f"Total entries: {len(df)} rows")
    except Exception as e:
        st.warning(f"Cannot display data: {e}")
