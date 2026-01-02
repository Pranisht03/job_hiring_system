import os
import docx
from PyPDF2 import PdfReader


def extract_text_from_cv(file_path):
    """
    Extract text from PDF or DOCX CV
    """
    text = ""

    if file_path.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + " "

    return text
