"""JSON REST API for external Angular / React frontends.

All endpoints are namespaced under /api and secured with JWT
(Flask-JWT-Extended). Session cookies used by the server-rendered pages are
completely separate from this API.
"""

import re

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from decorators import api_role_required
from extensions import db
from models import Role, User

api_bp = Blueprint("api", __name__, url_prefix="/api")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MIN_PASSWORD_LENGTH = 6


def _error(message, status=400):
    return jsonify({"error": message}), status


@api_bp.post("/auth/register")
def api_register():
    data = request.get_json(silent=True) or {}

    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or Role.USER).strip().lower()

    if not first_name or not last_name or not email or not password:
        return _error("first_name, last_name, email and password are required.")

    if not EMAIL_RE.match(email):
        return _error("Invalid email address.")

    if len(password) < MIN_PASSWORD_LENGTH:
        return _error(f"Password must be at least {MIN_PASSWORD_LENGTH} characters long.")

    if role not in Role.SELF_REGISTERABLE:
        return _error("Role must be 'user' or 'worker'.")

    if User.query.filter_by(email=email).first():
        return _error("An account with this email already exists.", status=409)

    user = User(first_name=first_name, last_name=last_name,
                email=email, role=role)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Registration successful.", "user": user.to_dict()}), 201


@api_bp.post("/auth/login")
def api_login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return _error("email and password are required.")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return _error("Invalid email or password.", status=401)

    if not user.is_active:
        return _error("This account has been disabled.", status=403)

    claims = {"role": user.role, "email": user.email}
    access_token = create_access_token(
        identity=str(user.id), additional_claims=claims)
    refresh_token = create_refresh_token(
        identity=str(user.id), additional_claims=claims)

    return jsonify(
        {
            "message": "Login successful.",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": user.to_dict(),
        }
    ), 200


@api_bp.post("/auth/refresh")
@jwt_required(refresh=True)
def api_refresh():
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity))

    if not user:
        return _error("User no longer exists.", status=404)

    claims = {"role": user.role, "email": user.email}
    access_token = create_access_token(
        identity=str(user.id), additional_claims=claims)

    return jsonify({"access_token": access_token}), 200


@api_bp.get("/auth/me")
@jwt_required()
def api_me():
    identity = get_jwt_identity()
    user = db.session.get(User, int(identity))

    if not user:
        return _error("User not found.", status=404)

    return jsonify({"user": user.to_dict()}), 200


@api_bp.get("/users")
@api_role_required(Role.ADMIN)
def api_list_users():
    """Admin-only: list every registered user."""
    users = User.query.order_by(User.id).all()
    return jsonify({"users": [u.to_dict() for u in users]}), 200


@api_bp.get("/users/<int:user_id>")
@jwt_required()
def api_get_user(user_id):
    """Fetch a single user's data.

    Admins may fetch any user; everyone else may only fetch their own record.
    """
    claims = get_jwt()
    identity = get_jwt_identity()

    if claims.get("role") != Role.ADMIN and int(identity) != user_id:
        return _error("Forbidden: insufficient permissions.", status=403)

    user = db.session.get(User, user_id)
    if not user:
        return _error("User not found.", status=404)

    return jsonify({"user": user.to_dict()}), 200
