from flask import Blueprint, render_template, request, flash, redirect , url_for, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash 
from werkzeug.datastructures import ImmutableMultiDict
from CloudApp.extensions import limiter, db
from CloudApp.models.user import User
from functools import wraps
import re
import uuid
import os

auth_bp = Blueprint("auth",__name__)

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
PASSWORD_REGEX = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{12,}$"

def validate_password(password):
    '''Validiert das Passwort'''
    if re.match(PASSWORD_REGEX, password):
        return True
    return False

def validate_email(email):
    '''Validiert die Email Adresse'''
    if re.match(EMAIL_REGEX, email):
        return True
    return False

def check_user(username):
        '''Prüft ob der Nutzername schon vergeben ist'''
        stmt = db.select(User).filter_by(username=username)
        check = db.session.execute(stmt).first() is not None
        return check

def check_mail(email):
        '''Prüft ob die Email Adresse schon vergeben ist'''
        stmt = db.select(User).filter_by(email = email)
        check = db.session.execute(stmt).first() is not None
        return check

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Sie sind bereits eingeloggt.", "info")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route("/register", methods=["GET","POST"])
@limiter.limit("5 per minute")
@logout_required
def register():
    """Registriert einen neuen Benutzer."""

    if request.method == "POST":
        
        username = request.form.get("username","").strip()
        email = request.form.get("email","").strip()
        email_check = request.form.get("email-check","").strip()
        password = request.form.get("password","")
        password_check = request.form.get("password-check","")
        agb = request.form.get("agb", "")
        dsgvo = request.form.get("dsgvo", "")
        
        form_dict = request.form.to_dict()

        ignore_fields = ['password', 'password-check']

        for field in ignore_fields:
            form_dict.pop(field, None)

        form_data = ImmutableMultiDict(form_dict)

        if len(username) < 3 or len(username) > 50:
            flash("Der Benutzername muss zwischen 3 und 50 Zeichen lang sein.", "error")
            return render_template("auth/register.html", form_data = form_data)

        elif len(email) > 254:
            flash("Die E-Mail-Adresse ist zu lang.", "error")
            return render_template("auth/register.html", form_data = form_data)

        elif len(password) > 128:
            flash("Das Passwort darf maximal 128 Zeichen lang sein.", "error")
            return render_template("auth/register.html", form_data = form_data)
        
        elif agb != "abg-accepted" and dsgvo != "dsgvo-accepted":
            flash("Bitte die AGB und die DSGVO akzeptieren!")
            return render_template("auth/register.html", form_data = form_data)
        
        elif not validate_email(email):
            flash("Bitte geben Sie eine gültige E-Mail-Adresse im Format beispiel@domain.de ein.", "error")
            return render_template("auth/register.html", form_data = form_data)
        
        elif email != email_check:
            flash("Ihre Email Adressen stimmen nicht überein!", "error")
            return render_template("auth/register.html", form_data = form_data)
        
        elif not validate_password(password):
            flash("Das Passwort muss mindestens 12 Zeichen, einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten!", "error")
            return render_template("auth/register.html", form_data = form_data)
        
        elif password != password_check:
            flash("Die eingegebenen Passwörter stimmen nicht überein", "error")
            return render_template("auth/register.html", form_data = form_data) 
                
        else:
            
            if check_user(username) or check_mail(email):
                generate_password_hash(password)
            
            else:
                base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
                directory_id = uuid.uuid4().hex
                new_user = User(username = username, email = email, directory_uuid = directory_id)
                new_user.set_password(password)
                db.session.add(new_user)
                path = os.path.join(base_path, directory_id)
                os.makedirs(path, exist_ok= True)
                db.session.commit()
                

            flash(f"Willkommen {username}! Danke für Ihre Registrierung!", "success")
            return redirect(url_for("auth.login"))            


    return render_template("auth/register.html", form_data={})

@auth_bp.route("/login", methods = ["GET", "POST"])
@limiter.limit("10 per minute")
@logout_required
def login():
    '''Loggt einen Benutzer ein'''

    if request.method == "POST":
        email = request.form.get("email").strip()
        password = request.form.get("password")

        stmt = db.select(User).filter_by(email = email)
        user = db.session.execute(stmt).scalar()
        
        if user:
            if user.check_password(password):
                login_user(user)
                return redirect(url_for("dashboard.dashboard"))
            else: 
                flash("Email oder Passwort falsch!","error")
        else:
            generate_password_hash(password) 
            flash("Email oder Passwort falsch!","error")

    return render_template("/auth/login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    '''Loggt eine Benutzer aus'''
    logout_user()
    flash("Sie haben sich erfolgreich abgemeldet!")
    return redirect(url_for("index"))