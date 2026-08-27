from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        '''Prüfen, ob der Nutzer eingeloggt ist UND Admin-Rechte hat'''
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403) 
        return f(*args, **kwargs)
    return decorated_function

def logout_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("Sie sind bereits eingeloggt.", "info")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def format_bytes(size):
    if not size:
        return "0 Bytes"
        
    size = float(size)
    units = ['Bytes', 'KB', 'MB', 'GB', 'TB']
    index = 0
    
    while size >= 1000 and index < len(units) - 1:
        size /= 1000.0
        index += 1
        
    return f"{round(size, 2)} {units[index]}"

