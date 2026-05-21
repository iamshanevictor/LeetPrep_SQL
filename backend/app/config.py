import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]


class Config:
    """Base application configuration."""

    APP_NAME = "LeetPrep-SQL"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'leetprep_sql.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    PROBLEMS_DIR = os.getenv("PROBLEMS_DIR", str(BASE_DIR / "problems"))
