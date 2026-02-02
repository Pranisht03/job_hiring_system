import os
import re
import docx
from PyPDF2 import PdfReader


def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_text_from_cv(file_field):
    """
    Accepts a FileField (profile.cv), not raw path
    """
    if not file_field:
        return ""

    try:
        file_path = file_field.path
    except Exception:
        return ""

    if not os.path.exists(file_path):
        return ""

    text = ""

    try:
        if file_path.endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""

        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "

    except Exception as e:
        print(f"CV parsing error: {e}")
        return ""

    return clean_text(text)
