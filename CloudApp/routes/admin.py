from flask import Blueprint, render_template, request, url_for, redirect, current_app, flash
from flask_login import login_required, current_user
from CloudApp.models.user import User
from CloudApp.models.file import File
from CloudApp.extensions import db
from CloudApp.services.utils import admin_required
from sqlalchemy import func
import os
import shutil

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@admin_required
def admin_dashboard():

    data = db.session.query(User, func.count(File.id), func.sum(File.file_size)).outerjoin(File).group_by(User.id).all()

    return render_template("admin.html", data = data)



@admin_bp.route("/toggle_lock/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_lock(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash("Du kannst dich nicht selbst sperren!", "error")
        return redirect(url_for('admin.admin_dashboard'))
        
    user.is_locked = not user.is_locked
    db.session.commit()
    
    status = "gesperrt" if user.is_locked else "entsperrt"
    flash(f"Nutzer {user.username} wurde {status}.", "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route("/delete_user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash("Du kannst deinen eigenen Admin-Account hier nicht löschen!", "error")
        return redirect(url_for('admin.admin_dashboard'))
        

    base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
    directory_path = os.path.join(base_path, user.directory_uuid)
    
    if os.path.exists(directory_path):
        try:
            shutil.rmtree(directory_path)
        except OSError as e:
            flash(f"Fehler beim Löschen der Dateien von {user.username}.", "error")
            return redirect(url_for('admin.admin_dashboard'))

    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f"Nutzer {username} und alle seine Dateien wurden endgültig gelöscht.", "success")
    return redirect(url_for('admin.admin_dashboard'))