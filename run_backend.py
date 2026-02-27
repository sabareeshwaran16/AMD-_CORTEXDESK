"""
Start CortexDesk Backend Server
Run this script to start the backend on http://localhost:8000
"""
import sys
import os

# Add backend to path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

print("=" * 50)
print("CortexDesk Backend Server")
print("=" * 50)
print()
print("Starting server on: http://localhost:8000")
print("API docs available at: http://localhost:8000/docs")
print()
print("Press Ctrl+C to stop")
print()

# Start the server
import uvicorn
from app.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
