# Screenshot OCR - Installation Guide

## Problem
Screenshot OCR is not working because **Tesseract OCR is not installed**.

## Diagnostic Results
- [OK] pytesseract Python module installed
- [OK] Pillow (PIL) Python module installed  
- [FAIL] Tesseract executable NOT found

## Solution: Install Tesseract OCR

### Option 1: Quick Install (Recommended)

1. **Download Tesseract installer:**
   https://github.com/UB-Mannheim/tesseract/wiki

2. **For Windows, download:**
   `tesseract-ocr-w64-setup-5.3.3.20231005.exe` (or latest version)

3. **Run installer** - use default location:
   `C:\Program Files\Tesseract-OCR`

4. **Add to PATH** (installer should do this automatically)
   - Or manually add: `C:\Program Files\Tesseract-OCR` to system PATH

5. **Restart your terminal/IDE**

6. **Test again:**
   ```bash
   python test_ocr.py
   ```

### Option 2: Manual Configuration (If PATH doesn't work)

If Tesseract is installed but still not found, configure the path manually:

**Edit:** `src/ocr/image_processor.py`

Add this at the top of the file:
```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Option 3: Use Without OCR (Temporary)

If you don't need OCR right now, the app will work fine for:
- Text files (.txt)
- PDFs with text
- Word documents (.docx)
- Excel files (.xlsx)

OCR is only needed for:
- Screenshots
- Scanned PDFs
- Images with text

## After Installation

1. **Restart API:**
   ```bash
   python src\api.py
   ```

2. **Test screenshot upload:**
   - Take a screenshot (Win+Shift+S)
   - Drag & drop to "Screen Capture OCR" area
   - Should extract text automatically

## Verify Installation

Run diagnostic:
```bash
python test_ocr.py
```

Should show:
```
[OK] pytesseract module found
[OK] Pillow module found
[OK] Tesseract found: version 5.x.x
[OK] OCR module working
[OK] ALL TESTS PASSED - OCR IS READY!
```

## Download Link

**Direct download:**
https://digi.bib.uni-mannheim.de/tesseract/

Choose the latest Windows installer (`.exe` file)
