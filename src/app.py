from flask import Flask, request, jsonify
import joblib
from src.classifier import extract_text_from_file
import logging

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'docx', 'txt', 'xlsx', 'xls', 'csv'}

model = joblib.load('model.joblib')
vectorizer = joblib.load('vectorizer.joblib')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_label(extracted_text):
    logger.info("Predicting label for extracted text.")
    # Vectorize the extracted text and predict the label
    text_vector = vectorizer.transform([extracted_text])
    predicted_label = model.predict(text_vector)
    return predicted_label[0]

@app.route('/classify_file', methods=['POST'])
def classify_file_route():
    logger.info("Received request to classify file.")
    
    if 'file' not in request.files:
        logger.warning("No file part in the request.")
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.warning("No file selected.")
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        logger.warning(f"File type {file.filename} not allowed.")
        return jsonify({"error": "File type not allowed"}), 400

    try:
        extracted_text = extract_text_from_file(file)
        logger.info(f"Extracted text from file: {file.filename}") 
        file_class = predict_label(extracted_text)
        logger.info(f"Predicted class for file: {file_class}")
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({"error": "Failed to process file"}), 500

    return jsonify({"file_class": file_class}), 200


if __name__ == '__main__':
    app.run(debug=True)
