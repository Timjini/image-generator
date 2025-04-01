import io
import pytest
from unittest.mock import patch
from flask import jsonify
from app.controllers.image_generator_controller import generate_image

@pytest.fixture
def mock_request():
    """Helper function to mock Flask request object."""
    class MockRequest:
        form = {}
        files = {}

    return MockRequest()


def test_generate_image_success(mock_request):
    """Test successful image processing."""
    mock_request.form = {"key": "test_key"}
    mock_request.files = {"image": (io.BytesIO(b"fake image data"), "test_image.jpg")}

    with patch("app.controllers.image_generator_controller.request", mock_request):
        response = generate_image()
        json_data, status_code = response

    assert status_code == 200
    assert json_data.json["message"] == "Image received"
    assert json_data.json["key"] == "test_key"
    assert json_data.json["filename"] == "test_image.jpg"


def test_generate_image_missing_key(mock_request):
    """Test when 'key' is missing in the request."""
    mock_request.form = {}
    mock_request.files = {"image": (io.BytesIO(b"fake image data"), "test_image.jpg")}

    with patch("app.controllers.image_generator_controller.request", mock_request):
        response = generate_image()
        json_data, status_code = response

    assert status_code == 400
    assert json_data.json["error"] == "Missing key or image"


def test_generate_image_missing_image(mock_request):
    """Test when 'image' is missing in the request."""
    mock_request.form = {"key": "test_key"}
    mock_request.files = {}

    with patch("app.controllers.image_generator_controller.request", mock_request):
        response = generate_image()
        json_data, status_code = response

    assert status_code == 400
    assert json_data.json["error"] == "Missing key or image"


def test_generate_image_empty_filename(mock_request):
    """Test when an empty filename is provided."""
    mock_request.form = {"key": "test_key"}
    mock_request.files = {"image": (io.BytesIO(b"fake image data"), "")}

    with patch("app.controllers.image_generator_controller.request", mock_request):
        response = generate_image()
        json_data, status_code = response

    assert status_code == 400
    assert json_data.json["error"] == "No image uploaded"
