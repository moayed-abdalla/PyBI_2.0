"""
Run Streamlit frontend
"""
import subprocess
import sys

if __name__ == "__main__":
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/main.py", "--server.port=8501"])

