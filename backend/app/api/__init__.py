from app.api.attempts import attempts_bp
from app.api.health import health_bp
from app.api.problems import problems_bp


def register_blueprints(app):
    """Register API blueprints with the Flask app."""
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(problems_bp, url_prefix="/api")
    app.register_blueprint(attempts_bp, url_prefix="/api")
