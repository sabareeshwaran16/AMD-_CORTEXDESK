# UPLOAD NOT WORKING - TROUBLESHOOTING

## Quick Test

1. Open `test_upload.html` in your browser
2. Select a file
3. Click Upload
4. Check if it works

If this works, the backend is fine. Issue is in the React app.

---

## Fix Steps

### 1. Check Backend is Running
Look for this in your backend terminal:
```
INFO:     Uvicorn running on http://127.0.0.1:8001
```

### 2. Test Backend Directly
```bash
python test_upload_endpoint.py
```

Should show:
```
Status: 200
Response: {'filename': '...', 'status': 'processing', ...}
```

### 3. Check Frontend Console
Open browser DevTools (F12) → Console tab
Look for errors when uploading

### 4. Check Network Tab
DevTools → Network tab → Try upload
- Does request reach backend?
- What's the response?
- Any CORS errors?

---

## Common Issues

### Issue: CORS Error
**Symptom:** Console shows "CORS policy" error

**Fix:** Backend already has CORS enabled. Clear browser cache.

### Issue: Network Error
**Symptom:** "ERR_CONNECTION_REFUSED"

**Fix:** Backend not running. Start it:
```bash
python src\api.py
```

### Issue: 500 Internal Server Error
**Symptom:** Upload fails with 500 error

**Check backend terminal for error details**

Possible causes:
- Missing dependencies
- File processing error
- Vector DB issue

---

## Manual Upload Test

```bash
# Test with curl
curl -X POST http://localhost:8001/upload -F "file=@test_upload_file.txt"
```

---

## What to Check

1. ✅ Backend running on port 8001
2. ✅ Frontend can reach http://localhost:8001
3. ✅ File size under 50MB
4. ✅ Supported format: PDF, DOCX, XLSX, PPTX, TXT
5. ✅ Browser console shows no errors

---

## Get Detailed Error

If upload fails, check:

**Backend Terminal:** Look for error messages
**Browser Console (F12):** Check for JavaScript errors
**Network Tab:** See actual request/response

Share the error message for specific help!
