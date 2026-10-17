from pathlib import Path
from werkzeug.security import generate_password_hash
from CloudApp.extensions import db
from CloudApp.models.user import User
from CloudApp.services.validate import validate_email , validate_password
from CloudApp.services.storage_service import StorageService
from sqlalchemy import or_ 
from sqlalchemy.exc import SQLAlchemyError

class UserValidationError(Exception):
    pass

class UserService:

    @staticmethod
    def is_username_taken(username :str) -> bool:
        stmt = db.select(User).filter_by(username=username)
        return db.session.execute(stmt).first() is not None
        
    @staticmethod
    def is_email_taken(email :str) -> bool:
        stmt = db.select(User).filter_by(email = email)
        return db.session.execute(stmt).first() is not None

    @classmethod
    def validate_username_input(cls, username :str) -> None:
        if len(username) < 3 or len(username) > 50:
            raise UserValidationError("Der Benutzername muss zwischen 3 und 50 Zeichen lang sein")
        if cls.is_username_taken(username):
            raise UserValidationError("Der Benutzername ist bereits vergeben")

    @staticmethod
    def validate_email_input(email :str, email_check :str) -> None:
        if len(email) > 254:
            raise UserValidationError("Die E-Mail Adresse ist zu lang.")
        if not validate_email(email):
            raise UserValidationError("Bitte geben Sie eine gültige E-Mail-Adresse im Format beispiel@domain.de ein.")
        if email != email_check:
            raise UserValidationError("Ihre Email Adressen stimmen nicht überein!")        

    @staticmethod
    def validate_password_input(password :str, password_check :str) -> None:
        if len(password) > 128:
            raise UserValidationError("Das Passwort darf maximal 128 Zeichen lang sein.")
        if not validate_password(password):
            raise UserValidationError(
                "Das Passwort muss mindestens 12 Zeichen, einen Großbuchstaben, "
                "einen Kleinbuchstaben, eine Zahl und ein Sonderzeichen enthalten!"
            )
        if password != password_check:
            raise UserValidationError("Die eingegebenen Passwörter stimmen nicht überein")

    @classmethod
    def register_user(cls, username: str, email: str, email_check: str, password: str, password_check: str, agb: str, dsgvo: str) -> User | None :
        """Validiert alle Eingaben und legt einen neuen Benutzer an-"""
        if agb != "agb-accepted" or dsgvo != "dsgvo-accepted":
            raise UserValidationError("Bitte die AGB und die DSGVO akzeptieren!")

        cls.validate_username_input(username)
        cls.validate_email_input(email, email_check)
        cls.validate_password_input(password, password_check)

        if cls.is_email_taken(email):
            generate_password_hash(password)
            return None

        new_user = User(
            username=username,
            email=email,
            agb_accepted=True,
            dsgvo_accepted=True
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def authenticate_user(login: str, password: str) -> User:
        stmt = db.select(User).where(
            or_(User.username == login, User.email == login)
        )
        user = db.session.execute(stmt).scalar_one_or_none()
        if not user:
            generate_password_hash(password)
            raise UserValidationError("Email oder Passwort falsch!")
        if not user.check_password(password):
            raise UserValidationError("Email oder Passwort falsch!")
        if user.is_locked:
            raise UserValidationError(
                "Dein Account wurde vom Administrator gesperrt. Bitte kontaktiere den Support."
            )

        return user

    @classmethod
    def update_username(cls,current_user: User, new_username: str, new_username_check: str) -> None:
        if new_username != new_username_check: 
            raise UserValidationError("Die Benutzernamen stimmen nicht überein")
        cls.validate_username_input(new_username)
        try:
            current_user.username = new_username
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise UserValidationError("Es ist ein Fehler aufgetreten.")

    @classmethod
    def update_email(cls, current_user: User, new_email: str, new_email_check: str) -> None:
        cls.validate_email_input(new_email, new_email_check)
        if cls.is_email_taken(new_email):
            raise UserValidationError("Die E-Mail Adresse ist bereits vergeben.")
        try:
            current_user.email = new_email
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise UserValidationError("Es ist ein Fehler aufgetreten.")


    @classmethod
    def update_password(cls, current_user: User, old_pasword: str, new_password: str, new_password_check: str ) -> None:
        if not current_user.check_password(old_pasword):
            raise UserValidationError("Sie haben ein falsches passwort eingegeben.")
        cls.validate_password_input(new_password, new_password_check)
        try:
            current_user.set_password(new_password)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise UserValidationError("Es ist ein Fehler aufgetreten")

    @classmethod
    def delete_account(cls, base_path: Path, current_user: User, password :str, password_check: str) -> None:
        if not current_user.check_password(password):
            raise UserValidationError("Sie haben ein falsches passwort eingegeben.")
        if password != password_check:
            raise UserValidationError("Die Passwörter stimmen nicht überein")
        directory_uuid = current_user.directory_uuid
        storage_service = StorageService(base_path)
        try: 
            db.session.delete(current_user)
            db.session.flush()
            storage_service.delete_user_folder(directory_uuid)
            db.session.commit()
        except (OSError, SQLAlchemyError):
            db.session.rollback()
            raise UserValidationError("Es ist ein Fehler aufgetreten.")