from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.datastructures import ImmutableMultiDict
from sqlalchemy.exc import SQLAlchemyError
from CloudApp.extensions import limiter, db
from CloudApp.services.user_service import UserService, UserValidationError
from CloudApp.services.utils import logout_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
@limiter.limit("5 per minute")
@logout_required
def register():
    """Registriert einen neuen Benutzer."""
    if request.method != "POST":
        return render_template("auth/register.html", form_data={})

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    email_check = request.form.get("email-check", "").strip()
    password = request.form.get("password", "")
    password_check = request.form.get("password-check", "")
    agb = request.form.get("agb", "")
    dsgvo = request.form.get("dsgvo", "")

    form_dict = request.form.to_dict()
    for field in ("password", "password-check"):
        form_dict.pop(field, None)
    form_data = ImmutableMultiDict(form_dict)

    try:
        UserService.register_user(
            username=username,
            email=email,
            email_check=email_check,
            password=password,
            password_check=password_check,
            agb=agb,
            dsgvo=dsgvo,
        )
        flash(f"Willkommen {username}! Danke für Ihre Registrierung!", "success")
        return redirect(url_for("auth.login"))

    except UserValidationError as err:
        flash(str(err), "error")
        return render_template("auth/register.html", form_data=form_data)

    except SQLAlchemyError:
        db.session.rollback()
        flash("Es ist ein Datenbankfehler aufgetreten. Bitte versuchen Sie es später erneut.", "error")
        return render_template("auth/register.html", form_data=form_data)


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
@logout_required
def login():
    """Loggt einen Benutzer ein."""
    if request.method == "POST":
        login_identifier = request.form.get("login", "").strip()
        password = request.form.get("password", "")

        try:
            user = UserService.authenticate_user(login_identifier, password)
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        except UserValidationError as err:
            flash(str(err), "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    """Loggt einen Benutzer aus."""
    logout_user()
    flash("Sie haben sich erfolgreich abgemeldet!")
    return redirect(url_for("index"))