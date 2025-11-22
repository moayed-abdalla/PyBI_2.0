📊 Dynamic KPI Dashboard Builder: PyBI 
A full-stack Python web application built with Flask and Streamlit, allowing users to upload data, build interactive dashboards, and visualize KPIs with modern UI. The backend is powered by Flask, the frontend by Streamlit, and the database by Supabase. The app is optimized for efficient SQL queries and responsive dark/light mode.

📁 Project File Structure
Organize your project with the following structure for clarity and maintainability:

```
pybi-dashboard/
│
├── app/                     # Main Flask application
│   ├── __init__.py
│   ├── routes.py            # Flask routes (API endpoints)
│   ├── models.py            # Database models (if using SQLAlchemy)
│   └── utils.py             # Utility functions (e.g., file upload, Supabase queries)
│
├── frontend/                # Streamlit frontend
│   ├── __init__.py
│   ├── main.py              # Streamlit dashboard entry point
│   ├── components/          # Custom UI components (e.g., KPI cards, chart popups)
│   │   ├── chart_config.py  # Chart configuration logic
│   │   └── sidebar.py       # Sidebar navigation
│   └── assets/
│       ├── favicon.ico      # Favicon file
│       └── PyBI_logo.png    # Logo file
│
├── supabase/                # Supabase config and migration scripts
│   ├── migrations/          # SQL migration scripts
│   └── config.py            # Supabase client setup
│
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables (never commit to GitHub)
├── .gitignore               # Ignore sensitive files
├── README.md                # This file
└── vercel.json              # Vercel deployment config
```

🛠️ Setup Instructions

1. Initialize the Project
Create a new directory for your project and set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Dependencies
Add the following to your requirements.txt:

```
Flask==3.0.3
streamlit==1.38.0
pandas==2.2.2
plotly==5.21.0
supabase==2.0.0
python-dotenv==1.0.1
gunicorn==21.2.0
```

Install dependencies:

```bash
pip install -r requirements.txt
```

🔌 Backend (Flask)

Flask App Structure
- `app/__init__.py`: Initialize the Flask app and configure Supabase.
- `app/routes.py`: Define API endpoints for file upload, dashboard management, and data retrieval.
- `app/utils.py`: Handle file uploads, Supabase queries, and data processing.

Example: Supabase Integration
```python
from flask import Flask
from supabase import create_client

app = Flask(__name__)

# Load Supabase credentials from .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

Key Endpoints
- `/upload`: Accept .csv or .xlsx files, store them in Supabase Storage, and return a reference ID.
- `/dashboards`: List, create, and manage dashboards.
- `/data/<dashboard_id>`: Retrieve data for a specific dashboard.

🖥️ Frontend (Streamlit)

Streamlit Dashboard Features
- **File Upload**: Support .csv and .xlsx uploads.
- **KPI Builder**: Add multiple KPIs (charts) with a "+" button.
- **Interactive Configuration**: Hover over charts to reveal a gear icon for settings (flip axes, remove labels/lines, delete chart).
- **Chart Types**: Integer metric (number), Bar, Line, Scatter, Pie.
- **Resizable Charts**: Drag to resize charts; add new charts beside or below.
- **Sidebar Navigation**: Toggle between dashboards.
- **Dark/Light Mode**: Automatically adapt to system settings with pre-registered color palettes.

Example: Chart Configuration Popup
```python
import streamlit as st

def chart_settings_popup():
    with st.popover("⚙️"):
        st.checkbox("Flip X/Y Axes")
        st.checkbox("Remove Labels")
        st.checkbox("Remove Lines")
        if st.button("Delete Chart"):
            # Logic to remove chart
            pass
```

🗄️ Database (Supabase)

Supabase Setup
- Create a Supabase project and database.
- Store uploaded files in Supabase Storage.
- Use SQL queries to efficiently retrieve and aggregate data for dashboards.

Example: SQL Query for KPI Data
```sql
SELECT 
    metric_name,
    SUM(value) as total_value,
    AVG(value) as avg_value
FROM kpi_data 
WHERE dashboard_id = '123'
GROUP BY metric_name;
```

🎨 UI/UX Details

Custom CSS
Inject custom CSS for a modern look:

```python
st.markdown(
    """
    <style>
    .stButton button {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stSidebar {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
```

Responsive Dark/Light Mode
- Use Plotly's built-in dark/light mode support.
- Pre-register color palettes for both modes.

🔗 External Links
Add your GitHub and Buy Me a Coffee links to the sidebar or footer:

```python
st.sidebar.markdown(
    """
    [GitHub](https://github.com/moayed-abdalla) | [Buy Me a Coffee](https://buymeacoffee.com/moayed_abdalla)
    """,
    unsafe_allow_html=True,
)
```

🚀 Deployment (Vercel)

Vercel Configuration
Use vercel.json to configure the deployment:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

Deploy with:

```bash
vercel
```

🛡️ Security & Optimization
- Store Supabase credentials in .env (never commit to GitHub).
- Use efficient SQL queries with indexing for performance.
- Validate and sanitize uploaded files to prevent security issues.
