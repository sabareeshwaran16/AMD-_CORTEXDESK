# SEARCH FIX - FINAL

## The Problem
Vector database is empty - need to add documents first!

## THE FIX - 3 Steps

### Step 1: RESTART API
```bash
# Stop API (Ctrl+C)
python src\api.py
```

### Step 2: ADD DATA
1. Open `cortexdesk.html`
2. Go to **Dashboard**
3. **Manual Entry** - paste this:

```
John needs to complete the database migration by Friday.
Sarah will update the API documentation.
Mike found a security bug.
Lisa is setting up testing.
```

4. Click **"Process Text"**
5. **Wait 5 seconds**

### Step 3: SEARCH
1. Go to **Research** page
2. Search for: `database`
3. Should work now!

## If Still Fails

The API needs restart after code changes:

```bash
# Terminal where API is running:
# Press Ctrl+C to stop
# Then:
python src\api.py
```

Then try Step 2 and 3 again.

## Quick Test

```bash
# After restarting API:
python quick_test.py
```

Should show: `[OK] Search works!`

---

**TL;DR:**
1. Restart API
2. Add data via Manual Entry  
3. Search

That's it!
