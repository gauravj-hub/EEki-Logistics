import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Eeki Logistics", layout="wide")

@st.cache_data(ttl=600)
def load_public_sheet(sheet_id, worksheet=0):
    """Load public Google Sheet as CSV"""
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet=Sheet{worksheet}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return df
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Make sure your Google Sheet is PUBLIC and use correct Sheet ID")
        return pd.DataFrame()

def main():
    st.title("🛒 Eeki Logistics Dashboard")
    
    # Get sheet ID from sidebar
    st.sidebar.header("📊 Sheet Settings")
    sheet_id = st.sidebar.text_input(
        "Google Sheet ID", 
        value="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"
    )
    
    df = load_public_sheet(sheet_id)
    
    if df.empty:
        st.warning("❌ No data loaded. Steps:")
        st.markdown("""
        1. Copy Sheet ID from your Google Sheet URL
        2. Make your Sheet **PUBLIC** (Anyone with link)
        3. Paste ID above and refresh
        """)
        return
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Rows", len(df))
    with col2: st.metric("Columns", len(df.columns))
    with col3: st.metric("Last Update", f"{pd.Timestamp.now():%H:%M}")
    
    st.markdown("---")
    
    # Data
    st.subheader("📋 Data")
    st.dataframe(df, use_container_width=True)
    
    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", csv, f"eeki_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.csv")

if __name__ == "__main__":
    main()
