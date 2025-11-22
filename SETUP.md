# 🛠️ PyBI Setup Guide

This guide will help you set up the PyBI Dashboard application from scratch.

## Prerequisites

- Python 3.8 or higher
- A Supabase account (free tier works)
- Git (optional)

## Step 1: Clone and Setup Environment

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Step 2: Supabase Setup

1. **Create a Supabase project:**
   - Go to [supabase.com](https://supabase.com)
   - Create a new project
   - Note your project URL and anon key

2. **Run database migrations:**
   - In Supabase Dashboard, go to SQL Editor
   - Copy and paste the contents of `supabase/migrations/001_initial_schema.sql`
   - Run the migration

3. **Create Storage Bucket:**
   - Go to Storage in Supabase Dashboard
   - Create a new bucket named `data-files`
   - Set it to public (or configure RLS policies as needed)

## Step 3: Environment Configuration

1. **Create a `.env` file** in the project root:
   ```bash
   cp env.example .env
   ```

2. **Edit `.env`** with your Supabase credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   SECRET_KEY=your-secret-key-here
   API_BASE_URL=http://localhost:5000/api
   ```

## Step 4: Streamlit Configuration

1. **Create `.streamlit/config.toml`** (optional):
   ```toml
   [server]
   port = 8501
   address = "localhost"
   ```

2. **Create `.streamlit/secrets.toml`** for Streamlit secrets:
   ```toml
   API_BASE_URL = "http://localhost:5000/api"
   ```

## Step 5: Run the Application

### Option 1: Run Flask and Streamlit separately (Recommended for development)

**Terminal 1 - Flask Backend:**
```bash
python run_flask.py
```
Backend will run on `http://localhost:5000`

**Terminal 2 - Streamlit Frontend:**
```bash
python run_streamlit.py
```
Frontend will run on `http://localhost:8501`

### Option 2: Use the main app.py (for Vercel deployment)
```bash
python app.py
```

## Step 6: Access the Application

1. Open your browser and go to `http://localhost:8501`
2. Create your first dashboard
3. Upload a CSV or Excel file
4. Start building your KPIs!

## Troubleshooting

### Common Issues:

1. **Import errors:**
   - Make sure you're in the virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **Supabase connection errors:**
   - Verify your `.env` file has correct credentials
   - Check that your Supabase project is active

3. **File upload errors:**
   - Ensure the `data-files` bucket exists in Supabase Storage
   - Check bucket permissions

4. **Port already in use:**
   - Change ports in `run_flask.py` or `run_streamlit.py`
   - Or kill the process using the port

## Next Steps

- Check out `QUICKSTART.md` for a quick tutorial
- Read `README.md` for detailed documentation
- Customize the UI and add more chart types as needed

