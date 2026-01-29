import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Eeki Logistics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=600)
def load_eeki_logistics_data():
    """Load logistics data from Google Sheet"""
    try:
        SHEET_ID = st.secrets["eeki_sheet_id"]
        
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Load service account from secrets
        creds_dict = st.secrets["gcp_service_account"]
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        client = gspread.authorize(creds)
        
        # Open sheet and get data
        sheet = client.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_records()
        
        if data:
            return pd.DataFrame(data)
        else:
            return pd.DataFrame()
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

def main():
    st.title("🛒 Eeki Logistics Dashboard")
    st.markdown("---")
    
    # Load data
    @st.cache_data(ttl=600)
    def get_data():
        return load_eeki_logistics_data()
    
    df = get_data()
    
    if df.empty:
        st.warning("No data found. Please check your Google Sheet ID and service account permissions.")
        st.info("Expected columns: Order_ID, Customer, Status, Date, Quantity, Destination")
        return
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    status_options = df['Status'].unique() if 'Status' in df.columns else []
    selected_status = st.sidebar.multiselect(
        "Status", 
        options=status_options, 
        default=status_options
    )
    
    if 'Date' in df.columns:
        date_range = st.sidebar.date_input("Date Range", [])
        if len(date_range) == 2:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df[(df['Date'] >= pd.to_datetime(date_range[0])) & 
                   (df['Date'] <= pd.to_datetime(date_range[1]))]
    
    # Apply status filter
    if selected_status:
        df = df[df['Status'].isin(selected_status)]
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_orders = len(df)
        st.metric("Total Orders", total_orders)
    
    with col2:
        if 'Quantity' in df.columns:
            total_qty = df['Quantity'].sum()
            st.metric("Total Quantity", total_qty)
    
    with col3:
        pending = len(df[df['Status'] == 'Pending']) if 'Status' in df.columns else 0
        st.metric("Pending Orders", pending)
    
    with col4:
        completed = len(df[df['Status'] == 'Completed']) if 'Status' in df.columns else 0
        st.metric("Completed", completed)
    
    st.markdown("---")
    
    # Data table
    st.subheader("📋 Logistics Data")
    st.dataframe(df, use_container_width=True)
    
    # Download button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"eeki_logistics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
