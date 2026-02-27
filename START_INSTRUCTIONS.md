# SIMPLE START GUIDE

## The 404 error means backend isn't running.

## DO THIS:

### Step 1: Start Backend
**Double-click:** `RUN_BACKEND_NOW.bat`

Wait until you see:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

**KEEP THIS WINDOW OPEN!**

---

### Step 2: Start Frontend
**Double-click:** `RUN_FRONTEND_NOW.bat`

Wait until you see:
```
Local: http://localhost:5173
```

Desktop app will open automatically.

---

## That's It!

- Backend window must stay open
- Frontend window must stay open
- Desktop app will work

---

## If Still 404:

Check backend is running:
1. Open browser
2. Go to: http://localhost:8001
3. Should see: `{"status": "running"}`

If you see that, refresh the desktop app.
