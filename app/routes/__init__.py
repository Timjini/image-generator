from flask import Blueprint
from .image_generator_routes import image_bp


api_bp = Blueprint("api", __name__, url_prefix="/api")
api_bp.register_blueprint(image_bp)

