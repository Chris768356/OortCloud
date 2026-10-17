from flask import Blueprint, render_template, redirect, request, url_for, flash, session, current_app
from flask_login import login_required, current_user, logout_user
from CloudApp.extensions import limiter
from CloudApp.services.user_service import UserService, UserValidationError


profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/")
@login_required
def show_profile():
    edit_mode = session.pop('edit_mode', None)
    return render_template("profile.html", edit_mode = edit_mode)


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
    new_username_check = request.form.get("confirm-username","").strip()

    try:
        UserService.update_username(current_user, new_username, new_username_check)
        flash("Benutzername erfolgreich geändert", "success")
        return redirect(url_for('profile.show_profile'))
    except UserValidationError as err:
        flash(str(err), "error")
        session['edit_mode'] = 'username'
        return redirect(url_for('profile.show_profile'))
    
@profile_bp.route("/change_mail", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def change_email():
    new_email  = request.form.get("mail","").strip()
    new_email_check = request.form.get("confirm-mail","").strip()
    try:
        UserService.update_email(current_user, new_email, new_email_check)
        flash("E-Mail Adresse erfolgreich geändert", "success")
        return redirect(url_for('profile.show_profile'))
    except UserValidationError as err:
        flash(str(err), "error")
        session['edit_mode'] = 'mail'
        return redirect(url_for('profile.show_profile'))

@profile_bp.route("/change_password", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def change_password():
    old_password = request.form.get("old-password","")
    new_password = request.form.get("password","")
    new_password_check = request.form.get("confirm-password","")

    try:
        UserService.update_password(current_user, old_password, new_password, new_password_check)
        flash("Ihr Passwort wurde erfolgreich geändert", "success")   
        return redirect(url_for('profile.show_profile')) 
    except UserValidationError as err:
        flash(str(err), "error")
        session['edit_mode'] = 'password'
        return redirect(url_for('profile.show_profile')) 
    
@profile_bp.route("/delete_profile", methods = ["POST"])
@login_required
@limiter.limit("10 per minute")
def delete_profile():
    password = request.form.get("password","")
    password_check = request.form.get("confirm-password","")
    username = current_user.username
    base_path = current_app.config.get("BASE_UPLOAD_FOLDER")

    try:
        UserService.delete_account(base_path, current_user, password, password_check)
    except UserValidationError as err:
        flash(str(err), "error")
        session['edit_mode'] = 'delete'
        return redirect(url_for('profile.show_profile'))

    flash(f"Schade das Sie uns verlassen {username}, Ihr Account wurde erfolgreich gelöscht!", "info")
    logout_user()
    return redirect(url_for('index')) 