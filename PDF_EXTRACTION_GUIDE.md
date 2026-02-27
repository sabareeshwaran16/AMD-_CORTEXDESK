# PDF Content Extraction Guide

## 🎯 Quick Methods

### Method 1: Automatic (via Upload)
```bash
# 1. Start backend
python src\api.py

# 2. Upload PDF via web interface or:
curl -X POST http://localhost:8001/upload -F "file=@your_file.pdf"
```

**What happens:**
- PDF text extracted automatically
- Tasks/actions identified
- Added to confirmation panel
- Indexed for search

---

### Method 2: Manual Extraction (Script)
```bash
python extract_pdf.py your_file.pdf
```

**Output:**
- Displays all text content
- Saves to `your_file_extracted.txt`

---

### Method 3: Python Code

```python
import pdfplumber

# Extract text from PDF
with pdfplumber.open('document.pdf') as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

---

## 📋 Complete Workflow

### Step 1: Extract Content
```bash
python extract_pdf.py meeting_notes.pdf
```

### Step 2: Review Extracted Text
```bash
# Opens in notepad
notepad meeting_notes_extracted.txt
```

### Step 3: Upload to System
```bash
# Via API
curl -X POST http://localhost:8001/upload -F "file=@meeting_notes.pdf"
```

### Step 4: Check Confirmations
```bash
# Open in browser
start confirmations.html
```

---

## 🔧 Advanced: Custom Extraction

### Extract Specific Pages
```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    # Extract only page 1
    text = pdf.pages[0].extract_text()
    
    # Extract pages 1-3
    text = ""
    for page in pdf.pages[0:3]:
        text += page.extract_text()
```

### Extract Tables
```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Extract with Metadata
```python
import pdfplumber

with pdfplumber.open('document.pdf') as pdf:
    print(f"Pages: {len(pdf.pages)}")
    print(f"Metadata: {pdf.metadata}")
    
    for i, page in enumerate(pdf.pages):
        text = page.extract_text()
        print(f"Page {i+1}: {len(text)} characters")
```

---

## 📊 What Gets Extracted

From your PDF, the system extracts:

✅ **Text Content:**
- Meeting notes
- Action items
- Decisions
- Deadlines

✅ **Structured Data:**
- Assignees (John, Sarah, Mike, Lisa)
- Dates (December 22, 2024, etc.)
- Priorities (HIGH, MEDIUM, LOW)
- Status (In Progress, Completed)

✅ **Tasks Identified:**
- "Complete the database migration by end of week"
- "Review and approve the new UI designs by Tuesday"
- "Schedule follow-up meeting with stakeholders"
- "Prepare presentation slides for client demo"

---

## 🎨 Create Your Own PDF

### Using Python (ReportLab)
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("my_document.pdf", pagesize=letter)
c.drawString(100, 750, "Meeting Notes")
c.drawString(100, 700, "Action: John complete report by Friday")
c.save()
```

### Using Word
1. Create document in Microsoft Word
2. Add your content
3. File → Save As → PDF

### Using Google Docs
1. Create document
2. File → Download → PDF

---

## 🚀 Test It Now

```bash
# Extract content from sample PDF
python extract_pdf.py sample_test_document.pdf

# View extracted content
type sample_test_document_extracted.txt

# Upload to system
curl -X POST http://localhost:8001/upload -F "file=@sample_test_document.pdf"

# Check confirmations
start confirmations.html
```

---

## 📝 Summary

**Automatic:** Upload PDF → System extracts → Tasks in confirmations
**Manual:** Run `extract_pdf.py` → Get text file
**Custom:** Use `pdfplumber` library in Python

All methods use the same underlying library: **pdfplumber**
