# SEARCH - COMPLETE EXAMPLE

## Step-by-Step Guide

### Step 1: Add Sample Data

**Open cortexdesk.html in your browser**

**Go to Dashboard → Manual Entry**

**Copy and paste this text:**

```
TEAM MEETING - January 2024

Project Updates:
- John needs to complete the database migration to PostgreSQL by Friday
- Sarah will update the API documentation by Monday  
- Mike is working on the new dashboard design
- Lisa will set up automated testing framework this week

Security Issues:
- Critical XSS vulnerability found in comment section - needs immediate fix
- Security audit scheduled for next month
- Need to implement two-factor authentication

Performance:
- Application is slow when loading large reports
- Need to optimize database queries
- Implement caching for frequently accessed data

Budget:
- Approved $50,000 for cloud infrastructure upgrade
- Hiring 2 new developers next quarter
- New office space lease signed

Decisions Made:
- Moving to React for frontend rewrite
- Postponing mobile app to Q2
- Weekly standup meetings every Monday at 10am
```

**Click "Process Text"**

**Wait 5 seconds** for processing

---

### Step 2: Go to Research Page

**Click "🔍 Research" in the sidebar**

---

### Step 3: Try These Searches

#### Search 1: `database`
**What you'll find:**
- John's database migration task
- PostgreSQL migration details
- Database query optimization

**Expected match:** 70-85%

---

#### Search 2: `security`
**What you'll find:**
- XSS vulnerability
- Security audit
- Two-factor authentication

**Expected match:** 65-80%

---

#### Search 3: `API documentation`
**What you'll find:**
- Sarah's documentation task
- API-related content

**Expected match:** 75-90%

---

#### Search 4: `performance optimization`
**What you'll find:**
- Slow report loading
- Database query optimization
- Caching implementation

**Expected match:** 60-75%

---

#### Search 5: `testing`
**What you'll find:**
- Lisa's automated testing task
- Testing framework setup

**Expected match:** 70-85%

---

#### Search 6: `budget`
**What you'll find:**
- Cloud infrastructure budget
- Hiring plans
- Office lease

**Expected match:** 65-80%

---

### What You Should See

For each search, results will look like:

```
Found 3 results for: "database"

Result 1                                    [82% match]
John needs to complete the database migration to 
PostgreSQL by Friday. The current MySQL setup has 
performance issues...
📄 Source: manual_entry_1234567890.txt

Result 2                                    [68% match]
Need to optimize database queries. Application is 
slow when loading large reports...
📄 Source: manual_entry_1234567890.txt
```

---

## More Sample Data (Optional)

### Sample 2: Technical Documentation

**Paste this in Manual Entry:**

```
SYSTEM ARCHITECTURE

Backend: Python FastAPI with SQLite database
Frontend: HTML, CSS, JavaScript
AI: Local LLM integration with Ollama
Storage: Encrypted SQLite with vector database

Features:
- Document processing (PDF, DOCX, XLSX, TXT)
- Meeting transcription and analysis
- Task extraction and management
- Semantic search with RAG
- Offline-first architecture

Security:
- All data encrypted at rest
- No cloud API calls
- Local processing only
- Zero telemetry

Performance:
- Vector search in under 100ms
- Document processing in 2-5 seconds
- Supports up to 10,000 documents
```

**Then search for:**
- `Python` → Find backend info
- `encryption` → Find security features
- `vector search` → Find search performance
- `document processing` → Find supported formats

---

### Sample 3: Project Tasks

**Paste this in Manual Entry:**

```
SPRINT TASKS - Week 1

High Priority:
- Fix login bug affecting 20% of users (Alex - Due: Tomorrow)
- Deploy hotfix for payment gateway (Maria - Due: Today)
- Complete security patch for user authentication (Tom - Due: Friday)

Medium Priority:
- Refactor user profile component (Sarah - Due: Next week)
- Update dependencies to latest versions (John - Due: Next week)
- Write unit tests for API endpoints (Lisa - Due: Next week)

Low Priority:
- Improve error messages in admin panel (Mike - Due: End of month)
- Add dark mode to settings page (Emma - Due: End of month)
- Update README documentation (David - Due: End of month)
```

**Then search for:**
- `login bug` → Find Alex's urgent task
- `payment` → Find Maria's hotfix
- `security patch` → Find Tom's task
- `unit tests` → Find Lisa's testing work
- `dark mode` → Find Emma's UI task

---

## Expected Results Summary

| Search Query | Expected Match | What You'll Find |
|--------------|----------------|------------------|
| database | 70-85% | Migration tasks, optimization |
| security | 65-80% | Vulnerabilities, audits |
| API | 75-90% | Documentation, endpoints |
| testing | 70-85% | Test frameworks, coverage |
| performance | 60-75% | Optimization, caching |
| Python | 70-85% | Backend architecture |
| urgent | 65-80% | High priority tasks |

---

## Troubleshooting

### "No results found"
- Make sure you clicked "Process Text"
- Wait 5 seconds after processing
- Try refreshing the page

### Low match scores (under 50%)
- API might not be restarted
- Run: `python src\api.py`
- Re-upload the data

### "Search failed" error
- Check API is running: `http://127.0.0.1:8001/`
- Check browser console (F12) for errors
- Restart API

---

## Quick Test Command

```bash
python quick_test.py
```

This will:
1. Upload sample data
2. Test search
3. Show match percentage

---

**Now try it! Copy the sample data above and search!** 🎉
