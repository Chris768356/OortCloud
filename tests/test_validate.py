from CloudApp.services.validate import validate_email, validate_password

def test_validate_email_valid():
    assert validate_email("test@beispiel.de") is True

def test_validate_email_invalid():
    assert validate_email("keine-email-adresse") is False
    assert validate_email("fehlt@domain") is False

def test_validate_password_rules():

    assert validate_password("Sicher!123456") is True

    assert validate_password("Kurz!1") is False

    assert validate_password("NurBuchstabenUnd123") is False