from flask import Blueprint, render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_required, current_user, logout_user
from CloudApp.extensions import db, limiter
from CloudApp.services.validate import validate_email, validate_password, check_mail, check_user
from CloudApp.models.user import User
import os
import shutil

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/")
@login_required
def show_profile():
    edit_mode = session.pop('edit_mode', None)
    return render_template("profile.html" ,edit_mode = edit_mode)


@profile_bp.route("/set_edit_mode", methods=["POST"])
@login_required
def set_edit_mode():
    target_mode = request.form.get("mode")
    if target_mode in ["username", "mail", "password", "delete"]:
        session['edit_mode'] = target_mode
    return redirect(url_for('profile.show_profile'))


@profile_bp.route("/change_username", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def change_username():
    new_username = request.form.get("username","").strip()
    confirm_username = request.form.get("confirm-username","").strip()
    if len(new_username) < 3 or len(new_username) > 50:
        flash("Der Benutzername muss zwischen 3 und 50 Zeichen lang sein.", "error")
        session['edit_mode'] = 'username'
        return redirect(url_for('profile.show_profile'))
    elif check_user(new_username):
        flash("Der Benutzername ist bereits vergeben.", "error")
        session['edit_mode'] = 'username'
        return redirect(url_for('profile.show_profile'))
    elif new_username != confirm_username:
        flash("Die Benutzernamen stimmen nicht überein!", "error")
        session['edit_mode'] = 'username'
        return redirect(url_for('profile.show_profile'))

    current_user.username = new_username
    db.session.commit()
    flash("Benutzername erfolgreich geändert", "success")
    return redirect(url_for('profile.show_profile'))


@profile_bp.route("/change_mail", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def change_email():
    new_email  = request.form.get("mail","").strip()
    confirm_email = request.form.get("confirm-mail","").strip()

    if len(new_email) > 254:
        flash("Die E-Mail-Adresse ist zu lang.", "error")
        session['edit_mode'] = 'mail'
        return redirect(url_for('profile.show_profile'))
    elif not validate_email(new_email):
        flash("Bitte geben Sie eine gültige E-Mail-Adresse im Format beispiel@domain.de ein.", "error")
        session['edit_mode'] = 'mail'
        return redirect(url_for('profile.show_profile'))
    elif check_mail(new_email):
        flash("Die E-Mail Adresse ist bereits vergeben, bitte wähle eine andere", "error")
        session['edit_mode'] = 'mail'
        return redirect(url_for('profile.show_profile'))
    elif new_email != confirm_email:
        flash("Die eingegebenen E-Mail Adressen stimmen nicht überein ", "error")
        session['edit_mode'] = 'mail'
        return redirect(url_for('profile.show_profile'))   

    current_user.email = new_email
    db.session.commit()  
    flash("E-Mail Adresse erfolgreich geändert", "success")
    return redirect(url_for('profile.show_profile'))
    
@profile_bp.route("/change_password", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def change_password():
    old_password = request.form.get("old-password","")
    new_password = request.form.get("password","")
    password_confirm = request.form.get("confirm-password","")

    if not current_user.check_password(old_password):
        flash("Das Aktuelle Passwort ist falsch!", "error")
        session['edit_mode'] = 'password'
        return redirect(url_for('profile.show_profile'))
    elif len(new_password) > 128:
        flash("Das Passwort darf maximal 128 Zeichen lang sein.", "error")
        session['edit_mode'] = 'password'
        return redirect(url_for('profile.show_profile'))
    elif not validate_password(new_password):
        flash("Das Passwort muss mindestens 12 Zeichen, einen Großbuchstaben, einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten!", "error")
        session['edit_mode'] = 'password'
        return redirect(url_for('profile.show_profile'))
    elif new_password != password_confirm:
        flash("Die eingegebenen Passwörter stimmen nicht überein", "error")
        session['edit_mode'] = 'password'
        return redirect(url_for('profile.show_profile'))      

    current_user.set_password(new_password)
    db.session.commit() 
    flash("Ihr Passwort wurde erfolgreich geändert", "success")   
    return redirect(url_for('profile.show_profile')) 

@profile_bp.route("/delete_profile", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def delete_profile():
    password = request.form.get("password","")
    password_confirm = request.form.get("confirm-password","")

    if not current_user.check_password(password):
        flash("Das Passwort ist falsch!", "error")
        session['edit_mode'] = 'delete'
        return redirect(url_for('profile.show_profile'))
    elif password != password_confirm:
        flash("Die Passwörter stimmen nicht überein!", "error")
        session['edit_mode'] = 'delete'
        return redirect(url_for('profile.show_profile'))

    
    
    base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
    user_uuid = current_user.directory_uuid
    directory_path = os.path.join(base_path, user_uuid)

    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
        except OSError as e:
            flash("Ein serverseitiger Fehler ist aufgetreten. Deine Dateien konnten nicht gelöscht werden.", "error")
            session['edit_mode'] = 'delete'
            return redirect(url_for('profile.show_profile'))

    flash(f"Schade das Sie uns verlassen {current_user.username}, Ihr Account wurde erfolgreich gelöscht!", "info")
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return redirect(url_for('index')) 