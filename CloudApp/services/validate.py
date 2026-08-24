from CloudApp.models.user import User
from CloudApp.extensions import db
import re


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
