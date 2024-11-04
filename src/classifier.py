from werkzeug.datastructures import FileStorage
import pytesseract
import cv2
import tempfile

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
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        file.save(temp_file.name)
        image = cv2.imread(temp_file.name)
        text = pytesseract.image_to_string(image)
    return text
