"""
OCR Image Processor
Extracts text from images using Tesseract OCR
"""
import os

def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        import pytesseract
        from PIL import Image
        
        # Open image
        image = Image.open(image_path)
        
        # Perform OCR
        text = pytesseract.image_to_string(image)
        
        return text.strip()
    except ImportError:
        # Tesseract not installed, return error message
        return "[OCR Error: Tesseract not installed. Install from: https://github.com/UB-Mannheim/tesseract/wiki]"
    except Exception as e:
        return f"[OCR Error: {str(e)}]"

def is_ocr_available():
    """Check if OCR is available"""
    try:
        import pytesseract
        from PIL import Image
        # Try to get tesseract version
        pytesseract.get_tesseract_version()
        return True
    except:
        return False
