# 🚀 PyBI Quick Start Guide

Get up and running with PyBI in 5 minutes!

## Quick Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Supabase:**
   - Create a `.env` file with your Supabase credentials (see `env.example`)
   - Run the SQL migration in Supabase Dashboard
   - Create a `data-files` storage bucket

3. **Start the servers:**
   ```bash
   # Terminal 1
   python run_flask.py
   
   # Terminal 2
   python run_streamlit.py
   ```

4. **Open your browser:**
   - Navigate to `http://localhost:8501`

## Your First Dashboard

1. **Create a Dashboard:**
   - Click "➕ Create New Dashboard" in the sidebar
   - Enter a name (e.g., "Sales Dashboard")
   - Click "Create"

2. **Upload Data:**
   - Click "📁 Upload Data File"
   - Select a CSV or Excel file
   - Click "Upload File"

3. **Add Charts:**
   - Click "➕ Add New Chart"
   - Choose a chart type (Bar, Line, Scatter, Pie, or Metric)
   - Select your X and Y columns
   - Click "Add Chart"

4. **Customize Charts:**
   - Hover over any chart and click the "⚙️" icon
   - Toggle options like "Flip X/Y Axes", "Remove Labels", etc.
   - Delete charts you don't need

## Example Data Format

Your CSV/Excel file should have columns like:

```
Date,Revenue,Expenses,Profit
2024-01-01,10000,5000,5000
2024-01-02,12000,5500,6500
2024-01-03,11000,5200,5800
```

## Chart Types

- **Metric**: Display a single number (sum or count)
- **Bar Chart**: Compare values across categories
- **Line Chart**: Show trends over time
- **Scatter Plot**: Explore relationships between variables
- **Pie Chart**: Show proportions

## Tips

- You can upload multiple files to the same dashboard
- Charts are automatically saved
- Switch between dashboards using the sidebar dropdown
- All data is stored securely in Supabase

## Need Help?

- Check `SETUP.md` for detailed setup instructions
- Read `README.md` for full documentation
- Visit the GitHub repository for issues and updates

Happy dashboarding! 📊

