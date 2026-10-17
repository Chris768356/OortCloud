import pytest
from CloudApp.extensions import db
from CloudApp.models.user import User
from CloudApp.services.user_service import UserService, UserValidationError
from CloudApp.services.storage_service import StorageService


@pytest.fixture
def sample_user(app):
    """Legt einen Standard-Testbenutzer für Update- und Lösch-Tests an."""
    with app.app_context():
        user = UserService.register_user(
            username="TestPilot",
            email="pilot@oortcloud.de",
            email_check="pilot@oortcloud.de",
            password="SuperSicher!123",
            password_check="SuperSicher!123",
            agb="agb-accepted",
            dsgvo="dsgvo-accepted",
        )
        return user.id


def test_register_and_authenticate_success(app):
    """Testet erfolgreiche Registrierung sowie Login per Benutzername und E-Mail."""
    with app.app_context():
        user = UserService.register_user(
            username="Commander",
            email="cmd@oortcloud.de",
            email_check="cmd@oortcloud.de",
            password="SuperSicher!123",
            password_check="SuperSicher!123",
            agb="agb-accepted",
            dsgvo="dsgvo-accepted",
        )
        assert user is not None
        assert user.username == "Commander"
        assert user.directory_uuid is not None

        # Login über Benutzername und über E-Mail prüfen
        auth_by_name = UserService.authenticate_user("Commander", "SuperSicher!123")
        auth_by_mail = UserService.authenticate_user("cmd@oortcloud.de", "SuperSicher!123")
        assert auth_by_name.id == user.id
        assert auth_by_mail.id == user.id


def test_register_duplicate_username_fails(app, sample_user):
    """Prüft, ob ein bereits vergebener Benutzername abgelehnt wird."""
    with app.app_context():
        with pytest.raises(UserValidationError, match="bereits vergeben"):
            UserService.register_user(
                username="TestPilot",
                email="neu@oortcloud.de",
                email_check="neu@oortcloud.de",
                password="SuperSicher!123",
                password_check="SuperSicher!123",
                agb="agb-accepted",
                dsgvo="dsgvo-accepted",
            )


def test_register_duplicate_email_returns_none_silently(app, sample_user):
    """Prüft den Schutz vor E-Mail-Enumeration (gibt None zurück statt Fehler)."""
    with app.app_context():
        result = UserService.register_user(
            username="NeuerName",
            email="pilot@oortcloud.de",
            email_check="pilot@oortcloud.de",
            password="SuperSicher!123",
            password_check="SuperSicher!123",
            agb="agb-accepted",
            dsgvo="dsgvo-accepted",
        )
        assert result is None


def test_authenticate_wrong_password_or_locked(app, sample_user):
    """Prüft Login-Ablehnung bei falschem Passwort und bei gesperrtem Account."""
    with app.app_context():
        # 1. Falsches Passwort
        with pytest.raises(UserValidationError, match="Passwort falsch"):
            UserService.authenticate_user("TestPilot", "FalschesPasswort!123")

        # 2. Gesperrter Account
        user = db.session.get(User, sample_user)
        user.is_locked = True
        db.session.commit()

        with pytest.raises(UserValidationError, match="gesperrt"):
            UserService.authenticate_user("TestPilot", "SuperSicher!123")


def test_update_username(app, sample_user):
    """Testet das Ändern des Benutzernamens inkl. Fehlerfall bei Abweichung."""
    with app.app_context():
        user = db.session.get(User, sample_user)

        with pytest.raises(UserValidationError, match="stimmen nicht überein"):
            UserService.update_username(user, "NeuerName", "TippfehlerName")

        UserService.update_username(user, "Captain", "Captain")
        assert db.session.get(User, sample_user).username == "Captain"


def test_update_email(app, sample_user):
    """Testet das Ändern der E-Mail-Adresse."""
    with app.app_context():
        user = db.session.get(User, sample_user)

        UserService.update_email(user, "captain@oortcloud.de", "captain@oortcloud.de")
        assert db.session.get(User, sample_user).email == "captain@oortcloud.de"


def test_update_password(app, sample_user):
    """Testet Passwortänderung und prüft, ob das alte Passwort korrekt abgefragt wird."""
    with app.app_context():
        user = db.session.get(User, sample_user)

        # Falsches altes Passwort muss fehlschlagen
        with pytest.raises(UserValidationError, match="falsches passwort"):
            UserService.update_password(user, "FalschAlt!123", "NeuSicher!456", "NeuSicher!456")

        # Erfolgreiche Änderung
        UserService.update_password(user, "SuperSicher!123", "NeuSicher!456", "NeuSicher!456")
        assert user.check_password("NeuSicher!456") is True


def test_delete_account_removes_user_and_folder(app, sample_user, tmp_path):
    """Prüft, ob delete_account sowohl den DB-Eintrag als auch den physischen Ordner löscht."""
    with app.app_context():
        user = db.session.get(User, sample_user)
        uuid_before = user.directory_uuid

        # Physischen Benutzerordner samt Testdatei anlegen
        storage = StorageService(tmp_path)
        user_folder = storage.get_user_folder(uuid_before)
        dummy_file = user_folder / "test.txt"
        dummy_file.write_text("Geheime Daten")
        assert user_folder.exists() is True

        # 1. Fehlversuch mit falschem Passwort (Ordner und User müssen erhalten bleiben)
        with pytest.raises(UserValidationError):
            UserService.delete_account(tmp_path, user, "FalschesPW!123", "FalschesPW!123")
        assert user_folder.exists() is True

        # 2. Erfolgreiche Löschung
        UserService.delete_account(tmp_path, user, "SuperSicher!123", "SuperSicher!123")

        assert db.session.get(User, sample_user) is None
        assert user_folder.exists() is False