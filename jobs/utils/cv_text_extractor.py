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


def extract_text_from_cv(cv_file):
    """
    Accepts either:
    - Django FileField (profile.cv)
    - or direct file path (string)
    """

    if not cv_file:
        return ""

    # 🔹 Determine file path safely
    if hasattr(cv_file, "path"):
        file_path = cv_file.path
    elif isinstance(cv_file, str):
        file_path = cv_file
    else:
        return ""

    if not os.path.exists(file_path):
        print("CV file not found:", file_path)
        return ""

    text = ""

    try:
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or ""

        elif file_path.lower().endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "

        else:
            print("Unsupported CV format:", file_path)

    except Exception as e:
        print("CV parsing error:", e)
        return ""

    return clean_text(text)
