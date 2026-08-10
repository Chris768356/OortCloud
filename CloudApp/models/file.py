from CloudApp.extensions import db
from datetime import datetime, timezone 
from werkzeug.utils import secure_filename

class File(db.Model):
    __tablename__ = "files"

    id = db.Column(db.Integer, primary_key = True)
    file_uuid = db.Column(db.String(36), unique = True, nullable = False, index =True)
    original_filename = db.Column(db.String(255), nullable = False)
    storage_filename = db.Column(db.String(255), unique = True, nullable = False)
    file_size = db.Column(db.BigInteger, nullable = False)
    uploaded_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)