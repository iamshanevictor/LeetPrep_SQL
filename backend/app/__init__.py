from flask import Flask
from flask_cors import CORS

from app.api import register_blueprints
from app.config import Config
from app.extensions import db


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.json.sort_keys = False

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    )
    db.init_app(app)
    register_blueprints(app)

    return app
