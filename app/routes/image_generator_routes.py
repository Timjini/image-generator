from flask import Blueprint
from app.controllers.image_generator_controller import generate_image

image_bp = Blueprint("image", __name__, url_prefix="/image")

image_bp.route("/generate", methods=["POST"])(generate_image)
