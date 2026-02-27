# HOW TO START CORTEXDESK

## Quick Start (2 Steps)

### Step 1: Start Backend Server
Open a terminal and run:
```bash
RUN_BACKEND.bat
```
Or:
```bash
python run_backend.py
```

Wait until you see: `Uvicorn running on http://127.0.0.1:8000`

### Step 2: Start Frontend (in a NEW terminal)
```bash
cd desktop
npm run dev
```

Wait until you see: `Local: http://localhost:5173`

### Step 3: Open Browser
Go to: **http://localhost:5173**

---

## Troubleshooting

### Backend won't start?
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-ai.txt
```

### Frontend won't start?
```bash
cd desktop
npm install
```

### Port already in use?
Kill the process:
```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F
```

---

## What Runs Where

- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend App**: http://localhost:5173

---

## Files to Run

✅ **RUN_BACKEND.bat** - Starts backend server
✅ **start_frontend.bat** - Starts frontend app
✅ **START_APP.bat** - Shows full instructions
