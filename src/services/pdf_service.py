import os
import base64
import pdfplumber
from io import BytesIO
from pypdf import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text.strip()

def convert_binary_to_text(cv_data):
    text = ""
    pdf_bytes = base64.b64decode(cv_data)

    with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

