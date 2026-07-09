"""Role-Based Access Control (RBAC) helpers.

Two flavours are provided:
- `login_required_web` / `role_required_web`: guard the server-rendered pages
  which rely on the Flask session set by the `/login` route.
- `api_role_required`: guard the JSON `/api/*` endpoints which rely on the
  JWT access token issued by `/api/auth/login`.
"""

from functools import wraps

from flask import abort, flash, jsonify, redirect, session, url_for
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def login_required_web(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def role_required_web(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to continue.", "error")
                return redirect(url_for("login"))
            if session.get("role") not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator


def api_role_required(*roles):
    """Require a valid JWT whose `role` claim is one of `roles`."""

    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims.get("role") not in roles:
                return jsonify({"error": "Forbidden: insufficient permissions."}), 403
            return view(*args, **kwargs)

        return wrapped

    return decorator
