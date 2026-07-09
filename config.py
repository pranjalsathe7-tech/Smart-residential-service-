import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Central application configuration, populated from environment variables."""

    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-me-please-32bytes")

    # Database (defaults to local SQLite so the app runs out of the box;
    # point DATABASE_URL at MySQL in production, e.g.
    # mysql+pymysql://<user>:<password>@<host>/<db_name>)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///smart_residential.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}

    # JWT (used only by the /api/* REST endpoints for Angular/React clients)
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "dev-jwt-secret-change-me-please-32b")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_TYPE = "Bearer"
    JWT_ERROR_MESSAGE_KEY = "error"

    # CORS - comma separated list of origins allowed to call the JSON API
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # Session cookie hardening (used for the server-rendered web pages)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get(
        "SESSION_COOKIE_SECURE", "false").lower() == "true"
