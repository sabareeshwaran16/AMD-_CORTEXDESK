# 🖥️ CortexDesk Desktop Application

## Quick Start

### Run Desktop App
```bash
START_DESKTOP.bat
```

This will:
1. Start backend server (port 8001)
2. Launch Electron desktop app

---

## What Changed

✅ **Before:** Web app in browser
✅ **Now:** Standalone desktop application

---

## Features

- Native desktop window
- System tray integration
- File dialogs (native OS)
- Runs without browser
- Auto-starts backend

---

## Manual Start

### Terminal 1 - Backend
```bash
python src\api.py
```

### Terminal 2 - Desktop App
```bash
cd desktop
npm run dev
```

---

## Build Standalone App

```bash
cd desktop
npm run build
```

Creates installable desktop app in `desktop/dist/`

---

## Status: ✅ Desktop Version Ready
