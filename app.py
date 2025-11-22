"""
Vercel deployment entry point
This file is used for Vercel serverless deployment
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

