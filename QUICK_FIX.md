# QUICK FIX - File Upload Issue

## The Problem
When uploading files (especially PPTX), the system fails with an import error.

## The Solution (1 minute fix)

### Option 1: Run the fix script
```bash
fix_upload.bat
```

### Option 2: Manual install
```bash
cd backend
pip install python-pptx==0.6.21
```

## What Was Wrong?
- Missing `python-pptx` package in `backend/requirements-ai.txt`
- File reader tries to import it for PPTX processing
- Now added and fixed ✓

## Test It
```bash
python test_upload_fix.py
```

## Start the Backend
```bash
cd backend
python -m app.main
```

The backend will run on http://localhost:8000

## Upload Files
1. Open desktop app or go to http://localhost:5173
2. Drag & drop files or click "Choose Files"
3. Supported: PDF, DOCX, XLSX, PPTX, TXT
4. Files are processed locally, tasks auto-extracted

## Status: ✓ RESOLVED
