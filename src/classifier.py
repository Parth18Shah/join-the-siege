from werkzeug.datastructures import FileStorage
import pytesseract
import cv2
import tempfile
import fitz
from docx import Document
import pandas as pd

def classify_file(file: FileStorage):
    filename = file.filename.lower()
    # file_bytes = file.read()

    if "drivers_license" in filename:
        return "drivers_license"

    if "bank_statement" in filename:
        return "bank_statement"

    
    if "invoice" in filename:
        return "invoice"

    return "unknown file"

def extract_text_from_file(file):
    filename = file.filename.lower()
    file_type = filename.split('.')[-1]

    if file_type in {'jpg', 'png'}:
        # Extract text from image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            file.save(temp_file.name)
            image = cv2.imread(temp_file.name)
            text = pytesseract.image_to_string(image)
        return text

    elif file_type == 'pdf':
        # Extract text from PDF
        return extract_text_from_pdf(file)

    elif file_type == 'docx':
        # Extract text from DOCX
        return extract_text_from_docx(file)

    elif file_type == 'txt':
        # Extract text from TXT
        return extract_text_from_txt(file)

    elif file_type in {'xlsx', 'xls'}:
        # Extract text from Excel files
        return extract_text_from_excel(file)
    
    elif file_type == 'csv':
        return extract_text_from_csv(file)

    else:
        return "Unsupported file type"

def extract_text_from_pdf(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        file.save(temp_pdf.name)
        text = ""
        pdf_document = fitz.open(temp_pdf.name)

        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text += page.get_text("text")

        pdf_document.close()
        return text

def extract_text_from_docx(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        file.save(temp_docx.name)
        doc = Document(temp_docx.name)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def extract_text_from_txt(file):
    text = file.read().decode('utf-8')
    return text

def extract_text_from_excel(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xls" if file.filename.endswith('.xls') else ".xlsx") as temp_xls:
        file.save(temp_xls.name)
        df = pd.read_excel(temp_xls.name)
        text = df.to_string(index=False)
    return text

def extract_text_from_csv(file):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_csv:
        file.save(temp_csv.name)
        df = pd.read_csv(temp_csv.name)
        text = df.to_string(index=False)
    return text