from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_required, current_user
from CloudApp.extensions import limiter, db
from werkzeug.utils import secure_filename
from sqlalchemy import func
from CloudApp.models.file import File
from CloudApp.models.user import User
import uuid
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
    max_user_memory = current_app.config.get("USER_QUOTA")
    
    if "uploaded_file" not in request.files:
        flash("Keine Datei gefunden", "error")
    else:
        file = request.files.get("uploaded_file")
        if file.filename == "":
            flash("Bitte wählen Sie eine Datei aus!","error")
        elif not check_file_extension(file.filename):
            flash("Dieser Dateityp ist nicht zulässig!", "error")
        else:
            original_name = secure_filename(file.filename)
            file_ext = original_name.rsplit('.', 1)[1].lower()
            file_uuid = uuid.uuid4().hex 
            storage_filename = file_uuid + "." + file_ext
            base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
            user_uuid = current_user.directory_uuid
            upload_folder = os.path.join(base_path, user_uuid, storage_filename)

            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)

            stmt = db.select(func.sum(File.file_size)).filter_by(user_id=current_user.id)
            used_user_memory = db.session.execute(stmt).scalar()

            if used_user_memory is None:
                used_user_memory = 0
            final_used_memory = file_size + used_user_memory

            if final_used_memory > max_user_memory:
                flash(f"Sie haben zu wenig verfügbaren Speicherplatz! {(final_used_memory / 1000 / 1000):.2f}MB / {(max_user_memory / 1000 / 1000):.2f}MB", "error")
                
            else:
                file.save(upload_folder)
                file_size = os.path.getsize(upload_folder)    
                new_file = File(file_uuid  = file_uuid, 
                                original_filename = original_name, 
                                storage_filename = storage_filename, 
                                file_size = file_size,
                                user_id = current_user.id)
                db.session.add(new_file)
                db.session.commit()            
                flash("Datei erfolgreich hochgeladen!", "success")
    return redirect(url_for("dashboard.dashboard"))

@dashboard_bp.route("/download/<string:file_uuid>")
@login_required
@limiter.limit("20 per minute")
def download(file_uuid):
    file_stmt = db.select(File).filter_by(file_uuid = file_uuid)
    file_record = db.session.execute(file_stmt).scalar()
    if not file_record or file_record.user_id != current_user.id:
        flash("Datei nicht gefunden.", "error")
        return redirect(url_for("dashboard.dashboard"))
    else:
        base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
        user_uuid = current_user.directory_uuid
        directory_path = os.path.join(base_path, user_uuid)

        return send_from_directory(
            directory=directory_path,
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
    
    else:
        try:
            base_path = current_app.config.get("BASE_UPLOAD_FOLDER")
            user_uuid = current_user.directory_uuid
            directory_path = os.path.join(base_path, user_uuid, file_record.storage_filename)
            if os.path.exists(directory_path):
                os.remove(directory_path)
            db.session.delete(file_record)
            db.session.commit()
            flash("Datei erfolgreich gelöscht!", "success")
        except:
            flash("Es ist ein Fehler aufgetreten!", "error")
    return redirect(url_for("dashboard.dashboard")) 