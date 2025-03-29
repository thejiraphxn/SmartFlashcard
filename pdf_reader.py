# pdf_reader.py
import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str, max_pages: int = 10) -> str:
    doc = fitz.open(file_path)
    text = ""
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        text += page.get_text()
    print(text)
    doc.close()
    return text
