"""
Extract content from PDF files
"""
import pdfplumber
import sys

def extract_pdf_content(pdf_path):
    """Extract all text from a PDF file"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text() or ""
                text += f"\n--- Page {page_num} ---\n{page_text}\n"
            return text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <pdf_file>")
        print("\nExample: python extract_pdf.py sample_test_document.pdf")
        sys.exit(1)
    
    pdf_file = sys.argv[1]
    print(f"Extracting content from: {pdf_file}\n")
    
    content = extract_pdf_content(pdf_file)
    print(content)
    
    # Save to text file
    output_file = pdf_file.replace('.pdf', '_extracted.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n[OK] Content saved to: {output_file}")
