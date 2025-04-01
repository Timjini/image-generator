from flask import request, jsonify
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = "uploads"

def generate_image():
    if "key" not in request.form or "image" not in request.files:
        return jsonify({"error": "Missing key or image"}), 400
    
    key = request.form["key"]
    image = request.files["image"]

    if image.filename == "":
        return jsonify({"error": "No image uploaded"}), 400
    
    filename = secure_filename(image.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    image.save(filepath)

    return jsonify({"message": "Image received", "key": key, "filename": filename}), 200
