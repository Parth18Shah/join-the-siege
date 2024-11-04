from io import BytesIO
from werkzeug.datastructures import FileStorage
import tempfile
import pytest
from src.app import app, allowed_file, predict_label
from scripts.generate_synthetic_data import generate_synthetic_data

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("filename, expected", [
    ("file.pdf", True),
    ("file.png", True),
    ("file.jpg", True),
    ("file.txt", True),
    ("file", False),
])
def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_no_file_in_request(client):
    response = client.post('/classify_file')
    assert response.status_code == 400

def test_no_selected_file(client):
    data = {'file': (BytesIO(b""), '')}  # Empty filename
    response = client.post('/classify_file', data=data, content_type='multipart/form-data')
    assert response.status_code == 400

def test_success(client, mocker):
    mocker.patch('src.app.classify_file_route', return_value='unknown file')

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
        temp_file.write(b"This is a test file content.")
        temp_file.seek(0)

        with open(temp_file.name, 'rb') as file:
            file_storage = FileStorage(stream=file, filename='test_file.txt', content_type='text/plain')

            data = {'file': file_storage}
            response = client.post('/classify_file', data=data, content_type='multipart/form-data')

            assert response.status_code == 200
            assert response.get_json() == {"file_class": "unknown file"}  

synthetic_data = generate_synthetic_data(5)

@pytest.mark.parametrize("file_content, expected_label", [
    (data["text_content"], data["label"]) for data in synthetic_data
])
def test_classification_model(file_content, expected_label):
    result = predict_label(file_content)
    assert result == expected_label

