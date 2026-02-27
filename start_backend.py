"""Start backend server"""
import sys
import os

# Set path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 50)
print("Starting CortexDesk Backend")
print("=" * 50)
print()

# Import and run
import uvicorn
from src.api import app

if __name__ == "__main__":
    print("Backend will run on: http://127.0.0.1:8001")
    print("Press Ctrl+C to stop")
    print()
    uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info")
