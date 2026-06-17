import subprocess
import sys
import time
import os

def run_app():
    # Start Backend
    print("Starting Backend (FastAPI)...")
    backend_process = subprocess.Popen(
        ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    # Wait for backend to be ready
    time.sleep(3)
    
    # Start Frontend
    print("Starting Frontend (Streamlit)...")
    frontend_process = subprocess.Popen(
        ["streamlit", "run", "frontend/streamlit_app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    
    try:
        while True:
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("Backend process terminated.")
                break
            if frontend_process.poll() is not None:
                print("Frontend process terminated.")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    run_app()
