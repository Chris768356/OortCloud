from CloudApp.extensions import db ,login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(254), unique = True, nullable = False)
    password_hash = db.Column(db.String(255), nullable = False)
    directory_uuid = db.Column(db.String(50), unique = True)
    created_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default = lambda: datetime.now(timezone.utc), onupdate = lambda: datetime.now(timezone.utc))
    files = db.relationship('File', backref='user')

    def set_password(self, password):
        """Hasht das Klartext-Passwort und speichert es in der Instanz."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Prüft, ob das eingegebene Passwort zum gespeicherten Hash passt."""
        return check_password_hash(self.password_hash, password)
    
@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login ruft diese Funktion bei jedem Seitenaufruf im Hintergrund auf.
    Es übergibt die ID aus dem Cookie (als String) und erwartet das User-Objekt.
    """
    return db.session.get(User, int(user_id))