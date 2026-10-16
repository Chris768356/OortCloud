import pytest
from CloudApp import create_app
from CloudApp.extensions import db

@pytest.fixture
def app(tmp_path):
   
    app = create_app({
        "TESTING": True,
        "SECRET_KEY": "test-secret-key",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "BASE_UPLOAD_FOLDER": str(tmp_path),
        "RATELIMIT_ENABLED": False,
        "WTF_CSRF_ENABLED": False,
        "USER_QUOTA": 5 * 1000 * 1000,
        "ALLOWED_EXTENSIONS": {"txt", "pdf", "png"}
    })

    assert "sqlite" in app.config["SQLALCHEMY_DATABASE_URI"], "STOPP: Tests laufen nicht auf SQLite!"

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()