from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory 
from flask_login import login_required, current_user
from CloudApp.extensions import limiter, db
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from CloudApp.models.file import File
from CloudApp.services.storage_service import StorageService
import os

dashboard_bp = Blueprint("dashboard",__name__)

def check_file_extension(filename):
    allowed = current_app.config.get("ALLOWED_EXTENSIONS")
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

@dashboard_bp.route("/")
@login_required
def dashboard():

    return render_template("dashboard.html")

@dashboard_bp.route("/upload", methods = ["POST"])
@limiter.limit("10 per minute")
@login_required
def upload():
    file = request.files.get("uploaded_file")
    max_user_memory = current_app.config.get("USER_QUOTA")
    if not file:
        flash("Keine Datei gefunden", "error")
        return redirect(url_for("dashboard.dashboard"))
    if not file.filename:
        flash("Bitte wählen Sie eine Datei aus!", "error")
        return redirect(url_for("dashboard.dashboard"))
    if not check_file_extension(file.filename):
        flash("Dieser Dateityp ist nicht zulässig!", "error")
        return redirect(url_for("dashboard.dashboard"))
        
    stmt = db.select(func.sum(File.file_size)).filter_by(user_id=current_user.id)
    used_user_memory = db.session.execute(stmt).scalar()

    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if used_user_memory is None:
            used_user_memory = 0
    final_used_memory = file_size + used_user_memory
    if final_used_memory > max_user_memory:
        flash(f"Sie haben zu wenig verfügbaren Speicherplatz! {(final_used_memory / 1000 / 1000):.2f}MB / {(max_user_memory / 1000 / 1000):.2f}MB", "error")
        return redirect(url_for("dashboard.dashboard"))
    
    storage_service  = StorageService(current_app.config.get("BASE_UPLOAD_FOLDER"))
    file_dto = storage_service.save_file(file, current_user.directory_uuid)
    
    new_file = File(file_uuid  = file_dto.uuid, 
            original_filename = file_dto.original_filename, 
            storage_filename = file_dto.storage_filename, 
            file_size = file_dto.file_size,
            user_id = current_user.id)
    db.session.add(new_file)
    
    try: 
        db.session.commit()            
        flash("Datei erfolgreich hochgeladen!", "success")
    except SQLAlchemyError:
        db.session.rollback()
        storage_service.delete_file(file_dto.storage_filename, current_user.directory_uuid)
        flash("Es ist ein fehler beim Speichern aufgetreten!", "error")

    return redirect(url_for("dashboard.dashboard"))



@dashboard_bp.route("/download/<string:file_uuid>")
@limiter.limit("20 per minute")
@login_required
def download(file_uuid):
    file_stmt = db.select(File).filter_by(file_uuid = file_uuid)
    file_record = db.session.execute(file_stmt).scalar()
    if not file_record or file_record.user_id != current_user.id:
        flash("Datei nicht gefunden.", "error")
        return redirect(url_for("dashboard.dashboard"))

    storage_service = StorageService(current_app.config.get("BASE_UPLOAD_FOLDER"))
    download_path = storage_service.get_file_path(file_record.storage_filename, current_user.directory_uuid)

    if download_path is None:
        flash("Datei nicht gefunden.", "error")
        return redirect(url_for("dashboard.dashboard"))
    
    return send_from_directory(
            directory=download_path.parent,
            path=file_record.storage_filename,
            as_attachment=True,
            download_name=file_record.original_filename
    )

    

@dashboard_bp.route("/delete/<string:file_uuid>", methods = ["POST"])
@login_required
def delete(file_uuid):
    file_stmt = db.select(File).filter_by(file_uuid = file_uuid)
    file_record = db.session.execute(file_stmt).scalar()

    if not file_record or file_record.user_id != current_user.id:
        flash("Datei nicht gefunden.", "error")
        return redirect(url_for("dashboard.dashboard"))
    
    storage_service = StorageService(current_app.config.get("BASE_UPLOAD_FOLDER"))

    try:
        storage_filename = file_record.storage_filename
        db.session.delete(file_record)
        db.session.commit()
        storage_service.delete_file(storage_filename, current_user.directory_uuid)
        flash("Datei erfolgreich gelöscht!", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Es ist ein Fehler aufgetreten!", "error")

    return redirect(url_for("dashboard.dashboard")) 