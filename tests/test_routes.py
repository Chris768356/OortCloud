import io
from CloudApp.models.user import User
from CloudApp.extensions import db

def test_register_and_login_flow(client, app):
  
    response = client.post("/auth/register", data={
        "username": "TestUser",
        "email": "test@oortcloud.de",
        "email-check": "test@oortcloud.de",
        "password": "SuperSicher!123",
        "password-check": "SuperSicher!123",
        "agb": "agb-accepted",
        "dsgvo": "dsgvo-accepted"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Willkommen TestUser" in response.get_data(as_text=True)


    with app.app_context():
        user = db.session.execute(db.select(User).filter_by(username="TestUser")).scalar()
        assert user is not None
        assert user.directory_uuid is not None


def test_upload_disallowed_extension(client, app):

    with app.app_context():
        user = User(username="Uploader", email="up@oortcloud.de", agb_accepted=True, dsgvo_accepted=True)
        user.set_password("SuperSicher!123")
        db.session.add(user)
        db.session.commit()

    client.post("/auth/login", data={"login": "Uploader", "password": "SuperSicher!123"})


    data = {
        "uploaded_file": (io.BytesIO(b"boeser code"), "malware.exe")
    }
    response = client.post("/dashboard/upload", data=data, content_type="multipart/form-data", follow_redirects=True)

    assert "Dieser Dateityp ist nicht zulässig!" in response.get_data(as_text=True)