from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class Role:
    """RBAC role constants used across web routes and the JSON API."""

    ADMIN = "admin"
    WORKER = "worker"
    USER = "user"

    ALL = (ADMIN, WORKER, USER)
    # Roles a visitor is allowed to self-register as. Admin accounts must be
    # provisioned separately (see the `flask create-admin` CLI command) so a
    # regular visitor can never grant themselves admin privileges.
    SELF_REGISTERABLE = (USER, WORKER)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default=Role.USER)
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc))

    def set_password(self, raw_password):
        self.password_hash = generate_password_hash(raw_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
            "phone": self.phone,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"
