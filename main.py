import secrets

import click
from flask import (
    Flask,
    flash,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from api_routes import api_bp
from config import Config
from decorators import login_required_web, role_required_web
from extensions import cors, db, jwt
from models import Role, User

SERVICES_LIST = ["Plumbing", "Electrician", "Cleaning", "Security"]

# Where each role lands after a successful login.
DASHBOARD_ENDPOINT = {
    Role.ADMIN: "admin",
    Role.WORKER: "worker",
    Role.USER: "user",
}


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    origins = app.config["CORS_ORIGINS"]
    if origins != "*":
        origins = [origin.strip()
                   for origin in origins.split(",") if origin.strip()]
    cors.init_app(app, resources={r"/api/*": {"origins": origins}})

    app.register_blueprint(api_bp)

    with app.app_context():
        db.create_all()

    register_web_routes(app)
    register_cli_commands(app)

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        return response

    return app


def register_web_routes(app):

    # ---------------- Auth / RBAC helpers ----------------
    @app.before_request
    def load_logged_in_user():
        user_id = session.get("user_id")
        g.current_user = db.session.get(User, user_id) if user_id else None

    @app.context_processor
    def inject_user():
        return {"current_user": g.get("current_user")}

    def generate_csrf_token():
        token = session.get("_csrf_token")
        if not token:
            token = secrets.token_urlsafe(32)
            session["_csrf_token"] = token
        return token

    app.jinja_env.globals["csrf_token"] = generate_csrf_token

    def csrf_valid():
        token = session.get("_csrf_token")
        submitted = request.form.get("csrf_token")
        return bool(token) and bool(submitted) and secrets.compare_digest(token, submitted)

    # ---------------- Public pages ----------------
    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/services")
    def services():
        return render_template("services.html", services=SERVICES_LIST)

    @app.route("/available")
    def available():
        return render_template("available.html", services=SERVICES_LIST)

    @app.route("/result")
    def result():
        return render_template("result.html")

    # ---------------- Authentication (session-based, for the web pages) ----------------
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            if not csrf_valid():
                flash("Your session has expired. Please try again.", "error")
                return render_template("login.html")

            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""

            if not email or not password:
                flash("Please enter both email and password.", "error")
                return render_template("login.html")

            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                flash("Invalid email or password.", "error")
                return render_template("login.html")

            if not user.is_active:
                flash("Your account has been disabled.", "error")
                return render_template("login.html")

            session.clear()
            session["user_id"] = user.id
            session["role"] = user.role

            flash(f"Welcome back, {user.first_name}!", "success")
            return redirect(url_for(DASHBOARD_ENDPOINT.get(user.role, "home")))

        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for("login"))

    @app.route("/Registration", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            if not csrf_valid():
                flash("Your session has expired. Please try again.", "error")
                return render_template("Registration.html")

            first_name = (request.form.get("first_name") or "").strip()
            last_name = (request.form.get("last_name") or "").strip()
            email = (request.form.get("email") or "").strip().lower()
            password = request.form.get("password") or ""
            role = (request.form.get("role") or Role.USER).strip().lower()

            if not first_name or not last_name or not email or not password:
                flash("Please fill in all fields.", "error")
                return render_template("Registration.html")

            if len(password) < 6:
                flash("Password must be at least 6 characters long.", "error")
                return render_template("Registration.html")

            if role not in Role.SELF_REGISTERABLE:
                flash("Invalid role selected.", "error")
                return render_template("Registration.html")

            if User.query.filter_by(email=email).first():
                flash("An account with this email already exists.", "error")
                return render_template("Registration.html")

            user = User(first_name=first_name, last_name=last_name,
                        email=email, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))

        return render_template("Registration.html")

    # ---------------- Dashboards (RBAC protected) ----------------
    @app.route("/admin")
    @role_required_web(Role.ADMIN)
    def admin():
        users = User.query.order_by(User.id).all()
        return render_template("admin.html", users=users)

    @app.route("/worker")
    @role_required_web(Role.WORKER)
    def worker():
        return render_template("worker_dashboard.html")

    @app.route("/user")
    @role_required_web(Role.USER)
    def user():
        return render_template("user_dashboard.html")

    @app.route("/profile")
    @login_required_web
    def profile():
        return render_template("profile.html")

    @app.route("/Service_Management")
    @role_required_web(Role.ADMIN, Role.WORKER)
    def Servicem():
        return render_template("Service_Management.html")

    # ---------------- Error handlers ----------------
    @app.errorhandler(403)
    def forbidden(_error):
        if request.path.startswith("/api"):
            return jsonify({"error": "Forbidden: insufficient permissions."}), 403
        flash("You do not have permission to view that page.", "error")
        return redirect(url_for("home"))

    @app.errorhandler(404)
    def not_found(_error):
        if request.path.startswith("/api"):
            return jsonify({"error": "Resource not found."}), 404
        return redirect(url_for("home"))


def register_cli_commands(app):
    @app.cli.command("create-admin")
    @click.option("--email", prompt=True)
    @click.option("--first-name", prompt="First name")
    @click.option("--last-name", prompt="Last name")
    @click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
    def create_admin(email, first_name, last_name, password):
        """Create (or promote) an admin account. Run: flask create-admin"""
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            user.role = Role.ADMIN
            user.set_password(password)
            click.echo(f"Existing user {email} promoted to admin.")
        else:
            user = User(first_name=first_name, last_name=last_name,
                        email=email, role=Role.ADMIN)
            user.set_password(password)
            db.session.add(user)
            click.echo(f"Admin user {email} created.")

        db.session.commit()


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
