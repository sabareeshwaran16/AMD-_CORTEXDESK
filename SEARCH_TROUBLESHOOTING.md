# Search Troubleshooting Guide

## Issue: Search Not Working

### Diagnostic Steps

1. **Check if API is running:**
   ```bash
   python test_search.py
   ```
   Should show: `[OK] API is running`

2. **Check vector database:**
   The test will show how many documents are indexed.
   If 0 documents, you need to upload files first.

3. **Open browser console:**
   - Press F12 in your browser
   - Go to "Console" tab
   - Try searching
   - Look for `[Search]` log messages

### Common Issues

#### Issue 1: "No results found"
**Cause:** No documents uploaded yet
**Solution:**
1. Go to Dashboard
2. Upload a document (PDF, TXT, DOCX)
3. Wait 5 seconds for processing
4. Try searching again

#### Issue 2: Search button does nothing
**Cause:** JavaScript error or API not running
**Solution:**
1. Check browser console (F12) for errors
2. Verify API is running: `python src\api.py`
3. Refresh the page (Ctrl+F5)

#### Issue 3: "Search failed" error
**Cause:** API connection issue
**Solution:**
1. Make sure API is running on port 8001
2. Check if another program is using port 8001
3. Try restarting the API

### Test Search Manually

1. **Start API:**
   ```bash
   python src\api.py
   ```

2. **Run test script:**
   ```bash
   python test_search.py
   ```

3. **Expected output:**
   ```
   [OK] API is running
   [OK] Vector DB found with 48 documents
   [OK] Found 5 results
   Top result: 8.97% match
   ```

### Debug in Browser

1. **Open cortexdesk.html**
2. **Press F12** (open developer tools)
3. **Go to Console tab**
4. **Try searching**
5. **Look for these messages:**
   ```
   [Search] Query: your search term
   [Search] Sending request to: http://127.0.0.1:8001/search
   [Search] Response status: 200
   [Search] Results: {count: 5, results: [...]}
   [Search] Results displayed successfully
   ```

### If Still Not Working

**Check these:**

1. **API URL correct?**
   - Open cortexdesk.html
   - Search for: `const API_URL`
   - Should be: `http://127.0.0.1:8001`

2. **CORS issue?**
   - Check browser console for CORS errors
   - API should have CORS enabled (it does)

3. **Port conflict?**
   - Try changing API port in `src/api.py`:
   ```python
   uvicorn.run(app, host="127.0.0.1", port=8002)  # Change to 8002
   ```
   - Update `cortexdesk.html`:
   ```javascript
   const API_URL = 'http://127.0.0.1:8002';
   ```

### Quick Test

Open browser console and run:
```javascript
fetch('http://127.0.0.1:8001/search', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({query: 'test'})
})
.then(r => r.json())
.then(d => console.log('Search result:', d))
.catch(e => console.error('Search error:', e));
```

Should show search results in console.

### Files to Check

- `cortexdesk.html` - Frontend code
- `src/api.py` - Backend search endpoint
- `data/vectors.pkl` - Vector database (should exist)
- Browser console (F12) - JavaScript errors

### Still Stuck?

1. Restart everything:
   ```bash
   # Stop API (Ctrl+C)
   python src\api.py
   ```

2. Clear browser cache (Ctrl+Shift+Delete)

3. Refresh page (Ctrl+F5)

4. Try search again with console open (F12)
