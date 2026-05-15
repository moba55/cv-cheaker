"""
CV PDF Text Extractor
---------------------
Reads a PDF file and outputs the extracted text.
Used as a standalone tool or called from n8n via "Execute Command" node.

Usage:
    python extract_cv.py path/to/cv.pdf
    python extract_cv.py path/to/cv.pdf --json
"""

import sys
import os
import json

def extract_text_with_pypdf2(pdf_path):
    """Extract text using PyPDF2 (lightweight, no dependencies)."""
    try:
        import PyPDF2
        text = ""
        with open(pdf_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text.strip()
    except ImportError:
        return None

def extract_text_with_pdfplumber(pdf_path):
    """Extract text using pdfplumber (better accuracy, handles tables)."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except ImportError:
        return None

def extract_text(pdf_path):
    """Try pdfplumber first, fall back to PyPDF2."""
    if not os.path.exists(pdf_path):
        return None, f"File not found: {pdf_path}"

    # Try pdfplumber first (better quality)
    text = extract_text_with_pdfplumber(pdf_path)
    if text is not None:
        return text, None

    # Fall back to PyPDF2
    text = extract_text_with_pypdf2(pdf_path)
    if text is not None:
        return text, None

    return None, "No PDF library found. Run: pip install pdfplumber"

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No PDF path provided. Usage: python extract_cv.py path/to/cv.pdf"}))
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_json = "--json" in sys.argv

    text, error = extract_text(pdf_path)

    if error:
        if output_json:
            print(json.dumps({"success": False, "error": error}))
        else:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    if output_json:
        # JSON output — used when called from n8n Execute Command node
        result = {
            "success": True,
            "text": text,
            "char_count": len(text),
            "word_count": len(text.split())
        }
        print(json.dumps(result, ensure_ascii=False))
    else:
        # Plain text output
        print(text)
