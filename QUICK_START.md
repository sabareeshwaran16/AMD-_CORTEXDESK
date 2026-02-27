# ⚡ QUICK START - CortexDesk

## ERR_CONNECTION_REFUSED Fix

The error means the backend server isn't running. Here's how to fix it:

---

## 🚀 EASIEST WAY - One Click

Double-click: **START_ALL.bat**

This opens 2 windows:
1. Backend Server (port 8000)
2. Frontend App (port 5173)

Wait 15 seconds, then open: **http://localhost:5173**

---

## 📋 MANUAL WAY - Two Terminals

### Terminal 1 - Backend
```bash
RUN_BACKEND.bat
```
Wait for: `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2 - Frontend
```bash
cd desktop
npm run dev
```
Wait for: `Local: http://localhost:5173`

### Browser
Open: **http://localhost:5173**

---

## ✅ What You Should See

**Backend Terminal:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Frontend Terminal:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

**Browser:**
- CortexDesk Dashboard with file upload area

---

## 🔧 Still Not Working?

### Install Dependencies

**Backend:**
```bash
cd backend
pip install -r requirements.txt
pip install -r requirements-ai.txt
```

**Frontend:**
```bash
cd desktop
npm install
```

### Check Ports
```bash
netstat -ano | findstr :8000
netstat -ano | findstr :5173
```

If ports are in use, kill the process or change ports in config.

---

## 📁 Files Created for You

- ✅ **START_ALL.bat** - Start everything (RECOMMENDED)
- ✅ **RUN_BACKEND.bat** - Backend only
- ✅ **start_frontend.bat** - Frontend only
- ✅ **run_backend.py** - Python backend starter
- ✅ **HOW_TO_START.md** - Detailed guide

---

## 🎯 Next Steps

1. Run **START_ALL.bat**
2. Wait 15 seconds
3. Open http://localhost:5173
4. Upload files and test!

**Status: Ready to run! 🚀**
