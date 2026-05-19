from flask import Blueprint, jsonify


attempts_bp = Blueprint("attempts", __name__)


@attempts_bp.get("/attempts")
def list_attempts():
    """Placeholder endpoint for future attempt tracking."""
    return jsonify({"attempts": []})
