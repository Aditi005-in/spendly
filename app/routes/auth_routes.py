from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.controllers.auth_controller import create_user
from app.models.user import User

auth = Blueprint("auth", __name__)


# -------------------- LOGIN --------------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

        session["user_id"] = user.id
        session["email"] = user.email

        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")



# -------------------- SIGNUP --------------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("signup.html")

        if create_user(first_name, last_name, email, password):
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("auth.login"))

        flash("Email already exists", "danger")

    return render_template("signup.html")


# -------------------- LOGOUT --------------------
@auth.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "info")
    return redirect(url_for("auth.login"))
