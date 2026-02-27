# SEARCH TEST GUIDE - Complete Walkthrough

## Step 1: Upload Sample Data

I've created 2 sample files for you:
- `data/uploads/sample_meeting.txt` - Project meeting notes
- `data/uploads/sample_documentation.txt` - Technical documentation

### Upload via Web UI:

1. **Open** `cortexdesk.html` in your browser
2. **Go to Dashboard**
3. **Click "Upload Document"** or drag & drop
4. **Upload both files:**
   - `sample_meeting.txt`
   - `sample_documentation.txt`
5. **Wait 5 seconds** for processing

### Or Upload via Manual Entry:

1. **Go to Dashboard**
2. **Find "Manual Entry" card**
3. **Copy this text:**
   ```
   Team meeting notes: John needs to complete the database migration by Friday. 
   Sarah will review the API documentation. Mike is working on the UI redesign.
   Lisa mentioned we need better test coverage for the payment module.
   Security audit scheduled for next month.
   ```
4. **Paste and click "Process Text"**

## Step 2: Test Search

### Go to Research Page

Click "🔍 Research" in the sidebar

### Try These Search Queries:

#### Query 1: "database migration"
**Expected:** Should find the meeting notes about PostgreSQL migration
**Look for:** John's task about database migration by Friday

#### Query 2: "API documentation"
**Expected:** Should find both meeting notes and technical docs
**Look for:** References to API endpoints and documentation updates

#### Query 3: "security"
**Expected:** Should find security-related content
**Look for:** XSS vulnerability, security audit, encryption features

#### Query 4: "testing"
**Expected:** Should find testing strategy and test coverage
**Look for:** Automated testing, QA tasks, test coverage requirements

#### Query 5: "performance"
**Expected:** Should find performance optimization content
**Look for:** Page load time, optimization strategies, FAISS

#### Query 6: "John"
**Expected:** Should find tasks assigned to John
**Look for:** Database migration, API docs, XSS fix

## Step 3: Verify Results

### Each result should show:
- ✅ Match percentage (e.g., "85% match")
- ✅ Text preview (first 500 characters)
- ✅ Source file name
- ✅ Ranked by relevance (highest match first)

### Example Expected Output:

```
Found 3 results for: "database migration"

Result 1                                    [92% match]
John mentioned that the database migration to PostgreSQL 
needs to be completed by Friday. The current MySQL setup 
is causing performance issues...
📄 Source: sample_meeting.txt

Result 2                                    [78% match]
INSTALLATION REQUIREMENTS Python Dependencies: fastapi, 
uvicorn, pydantic, python-multipart, PyPDF2...
📄 Source: sample_documentation.txt
```

## Step 4: Debug (If Not Working)

### Open Browser Console (F12)

You should see:
```
[Search] Query: database migration
[Search] Sending request to: http://127.0.0.1:8001/search
[Search] Response status: 200
[Search] Results: {count: 3, results: [...]}
[Search] Results displayed successfully
```

### If You See Errors:

**"No results found"**
- Upload the sample files first
- Wait 5 seconds after upload
- Try searching again

**"Search failed: 404"**
- API not running
- Run: `python src\api.py`

**"Search failed: Network error"**
- Check API is on port 8001
- Try: `http://127.0.0.1:8001/` in browser
- Should show: `{"name":"Local AI Workspace Assistant"...}`

## Step 5: Test Backend Directly

Run this in terminal:
```bash
python test_search.py
```

Should show:
```
[OK] API is running
[OK] Vector DB found with 50+ documents
[OK] Found 5 results
Top result: 85% match
```

## Quick Test Commands

### Test 1: Upload sample data
```bash
# API should be running
# Then upload via web UI
```

### Test 2: Search via Python
```python
import requests
response = requests.post(
    'http://127.0.0.1:8001/search',
    json={'query': 'database migration'}
)
print(response.json())
```

### Test 3: Check vector DB
```bash
python -c "import pickle; data=pickle.load(open('data/vectors.pkl','rb')); print(f'Documents: {len(data[\"vectors\"])}')"
```

## Expected Behavior

### After uploading sample files:
- ✅ 2 new documents in vector database
- ✅ Search returns relevant results
- ✅ Results ranked by similarity
- ✅ Source files displayed correctly

### Search should work for:
- ✅ Exact keywords ("database", "API")
- ✅ Phrases ("database migration")
- ✅ Concepts ("security", "performance")
- ✅ Names ("John", "Sarah")
- ✅ Technical terms ("FastAPI", "SQLite")

## Troubleshooting Checklist

- [ ] API is running (`python src\api.py`)
- [ ] Sample files uploaded
- [ ] Waited 5 seconds after upload
- [ ] Browser console open (F12)
- [ ] No JavaScript errors in console
- [ ] Vector DB exists (`data/vectors.pkl`)
- [ ] Vector DB has documents (run test_search.py)

## Success Criteria

✅ Upload 2 sample files
✅ Search for "database migration"
✅ See 2-3 results with match percentages
✅ Results show text preview and source file
✅ No errors in browser console

---

**Ready to test? Follow Step 1 above!**
