"""Shared Flask extension instances.

Kept in their own module (instead of main.py) so that models.py, api_routes.py
and decorators.py can import them without causing circular imports.
"""

from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS()
