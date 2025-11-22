import streamlit as st
import requests
from typing import List, Dict, Any, Optional

API_BASE_URL = st.secrets.get("API_BASE_URL", "http://localhost:5000/api")

def get_dashboards() -> List[Dict[str, Any]]:
    """Fetch all dashboards from API"""
    try:
        response = requests.get(f"{API_BASE_URL}/dashboards")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching dashboards: {str(e)}")
        return []

def create_dashboard(name: str, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Create a new dashboard"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/dashboards",
            json={"name": name, "description": description}
        )
        if response.status_code == 201:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Error creating dashboard: {str(e)}")
        return None

def render_sidebar():
    """Render the sidebar with dashboard navigation"""
    try:
        st.sidebar.image("PyBI_logo.png", use_container_width=True)
    except:
        pass
    st.sidebar.title("📊 PyBI Dashboard")
    
    # Get dashboards
    dashboards = get_dashboards()
    
    # Dashboard selection
    if dashboards:
        dashboard_names = [d['name'] for d in dashboards]
        selected_name = st.sidebar.selectbox(
            "Select Dashboard",
            dashboard_names,
            key="dashboard_selector"
        )
        selected_dashboard = next((d for d in dashboards if d['name'] == selected_name), None)
    else:
        selected_dashboard = None
        st.sidebar.info("No dashboards yet. Create one below!")
    
    st.sidebar.divider()
    
    # Create new dashboard
    with st.sidebar.expander("➕ Create New Dashboard"):
        with st.form("create_dashboard_form"):
            new_name = st.text_input("Dashboard Name", key="new_dashboard_name")
            new_description = st.text_area("Description (optional)", key="new_dashboard_description")
            submit = st.form_submit_button("Create")
            
            if submit:
                if new_name:
                    dashboard = create_dashboard(new_name, new_description)
                    if dashboard:
                        st.success(f"Dashboard '{new_name}' created!")
                        st.rerun()
                else:
                    st.error("Please enter a dashboard name")
    
    st.sidebar.divider()
    
    # External links
    st.sidebar.markdown(
        """
        **Links:**
        - [GitHub](https://github.com/moayed-abdalla)
        - [Buy Me a Coffee](https://buymeacoffee.com/moayed_abdalla)
        """
    )
    
    return selected_dashboard

