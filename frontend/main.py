import streamlit as st
import pandas as pd
import requests
from typing import Dict, Any, Optional, List
from frontend.components.sidebar import render_sidebar
from frontend.components.chart_config import render_chart_editor, create_chart

# Page configuration
st.set_page_config(
    page_title="PyBI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown(
    """
    <style>
    .stButton button {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    .stSidebar {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:5000/api")

def get_dashboard_data(dashboard_id: str) -> Optional[pd.DataFrame]:
    """Fetch data for a dashboard"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboards/{dashboard_id}/data")
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                return pd.DataFrame(data['data'])
        return None
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def get_charts(dashboard_id: str) -> List[Dict[str, Any]]:
    """Fetch charts for a dashboard"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboards/{dashboard_id}/charts")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching charts: {str(e)}")
        return []

def save_chart(dashboard_id: str, chart_config: Dict[str, Any]) -> bool:
    """Save chart configuration"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/dashboards/{dashboard_id}/charts",
            json=chart_config
        )
        return response.status_code == 201
    except Exception as e:
        st.error(f"Error saving chart: {str(e)}")
        return False

def upload_file(dashboard_id: str, file) -> bool:
    """Upload a file to the dashboard"""
    try:
        # Reset file pointer to beginning
        file.seek(0)
        files = {'file': (file.name, file.getvalue(), file.type)}
        response = requests.post(
            f"{API_BASE_URL}/dashboards/{dashboard_id}/upload",
            files=files
        )
        if response.status_code == 201:
            return True
        else:
            error_msg = response.json().get('error', 'Unknown error')
            st.error(f"Upload failed: {error_msg}")
            return False
    except Exception as e:
        st.error(f"Error uploading file: {str(e)}")
        return False

def render_add_chart_form(df: pd.DataFrame, dashboard_id: str):
    """Render form to add a new chart"""
    with st.expander("➕ Add New Chart", expanded=False):
        with st.form("add_chart_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                chart_type = st.selectbox(
                    "Chart Type",
                    ["metric", "bar", "line", "scatter", "pie"],
                    key="new_chart_type"
                )
                chart_title = st.text_input("Chart Title", key="new_chart_title")
            
            with col2:
                if chart_type == "metric":
                    metric_column = st.selectbox(
                        "Metric Column",
                        [""] + list(df.columns),
                        key="new_metric_column"
                    )
                    x_column = None
                    y_column = None
                else:
                    x_column = st.selectbox(
                        "X Column",
                        [""] + list(df.columns),
                        key="new_x_column"
                    )
                    y_column = st.selectbox(
                        "Y Column",
                        [""] + list(df.columns),
                        key="new_y_column"
                    )
                    metric_column = None
            
            submit = st.form_submit_button("Add Chart", type="primary")
            
            if submit:
                if chart_type == "metric":
                    if not metric_column:
                        st.error("Please select a metric column")
                    else:
                        chart_config = {
                            'chart_type': chart_type,
                            'chart_title': chart_title or metric_column,
                            'metric_column': metric_column,
                            'config': {},
                            'position': len(get_charts(dashboard_id))
                        }
                        if save_chart(dashboard_id, chart_config):
                            st.success("Chart added!")
                            st.rerun()
                else:
                    if not x_column or not y_column:
                        st.error("Please select both X and Y columns")
                    else:
                        chart_config = {
                            'chart_type': chart_type,
                            'chart_title': chart_title or f"{chart_type.title()} Chart",
                            'x_column': x_column,
                            'y_column': y_column,
                            'config': {},
                            'position': len(get_charts(dashboard_id))
                        }
                        if save_chart(dashboard_id, chart_config):
                            st.success("Chart added!")
                            st.rerun()

def main():
    """Main application"""
    # Render sidebar
    selected_dashboard = render_sidebar()
    
    if not selected_dashboard:
        st.info("👈 Please create or select a dashboard from the sidebar to get started!")
        return
    
    dashboard_id = selected_dashboard['id']
    dashboard_name = selected_dashboard['name']
    
    st.title(f"📊 {dashboard_name}")
    
    # File upload section
    with st.expander("📁 Upload Data File", expanded=False):
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            key="file_uploader"
        )
        
        if uploaded_file is not None:
            if st.button("Upload File", type="primary"):
                with st.spinner("Uploading file..."):
                    if upload_file(dashboard_id, uploaded_file):
                        st.success("File uploaded successfully!")
                        st.rerun()
    
    # Get dashboard data
    df = get_dashboard_data(dashboard_id)
    
    if df is None or df.empty:
        st.info("📊 No data available. Please upload a data file to get started!")
        return
    
    # Display data info
    st.info(f"📈 Data loaded: {len(df)} rows, {len(df.columns)} columns")
    
    # Show data preview
    with st.expander("👀 Preview Data"):
        st.dataframe(df.head(10), use_container_width=True)
    
    st.divider()
    
    # Get existing charts
    charts = get_charts(dashboard_id)
    
    # Add chart form
    if not df.empty:
        render_add_chart_form(df, dashboard_id)
    
    st.divider()
    
    # Render charts
    if charts:
        st.subheader("📊 Charts")
        
        # Render charts in a grid layout
        for i, chart_config in enumerate(charts):
            with st.container():
                render_chart_editor(df, chart_config, dashboard_id)
                if i < len(charts) - 1:
                    st.divider()
    else:
        st.info("➕ No charts yet. Add your first chart using the form above!")

if __name__ == "__main__":
    main()

