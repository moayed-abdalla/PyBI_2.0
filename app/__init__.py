import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from supabase.config import supabase

load_dotenv()

def create_app():
    """Initialize Flask application"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Enable CORS for Streamlit frontend
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Register routes
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app

