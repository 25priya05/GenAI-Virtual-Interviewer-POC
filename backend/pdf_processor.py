from dotenv import load_dotenv
load_dotenv()

import fitz  # PyMuPDF

def extract_pdf_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

