# ☁️ OortCloud

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-success)

OortCloud ist eine hochsichere, minimalistische Cloud-Speicher-Webapplikation. Sie ermöglicht authentifizierten Nutzern einen isolierten und privaten Speicherraum zum Hochladen, Verwalten und Teilen von Dateien. Ein zentraler Fokus der Architektur liegt auf strenger Datentrennung, Netzwerksicherheit und performanter Datenbankmodellierung.

> **Hinweis:** Dies ist ein Portfolio-Projekt zur Demonstration von Backend-Architektur, sicherem Datei-Handling und relationaler Datenbankmodellierung.

---

## ✨ Features

* **Sichere Datei-Isolierung:** Jeder Nutzer erhält ein physisch getrenntes Verzeichnis auf dem Server. Die Auslieferung erfolgt maskiert über UUIDv4-Token – physische Dateipfade werden niemals an den Client gesendet (Schutz vor IDOR-Angriffen).
* **Smartes Dashboard:** Übersichtliche Darstellung des Speicherkontingents, dynamische Datei-Icons (via Font Awesome) und Größenberechnung in Echtzeit.
* **Account-Management:** Sichere Authentifizierung, gehashte Passwörter (Werkzeug Security) und eine DSGVO-konforme Löschfunktion (Automatisches Cascading in der Datenbank + vollständige physische Bereinigung des Nutzerverzeichnisses).
* **Admin-Panel:** Rollenbasiertes Zugriffssystem (RBAC) zur Verwaltung von Nutzern und System-Ressourcen.
* **Sicherheits-Fokus:** Implementierung strenger OWASP-Richtlinien (CSP, X-Frame-Options, Cache-Control, Dateinamen-Sanitization).

---

## 🛠️ Technologie-Stack

* **Backend:** Python 3, Flask (Application Factory Pattern)
* **Datenbank:** MySQL / MariaDB (InnoDB)
* **ORM & Migrationen:** SQLAlchemy, Flask-Migrate (Alembic), PyMySQL
* **Frontend:** HTML5, CSS3, Jinja2, Font Awesome

---

## 🔒 Sicherheitsarchitektur

Das System implementiert proaktiv Schutzmaßnahmen auf Netzwerk- und Applikationsebene:

1. **HTTP Security Headers:** Strikte `Content-Security-Policy` (CSP) und `X-Frame-Options` blockieren XSS und Clickjacking.
2. **Cache-Control:** Geschützte Routen senden `no-store, no-cache, must-revalidate`, um unautorisierten Zugriff über den Browser-Verlauf nach dem Logout zu verhindern.
3. **Path Traversal Prevention:** Uploads werden serverseitig über `werkzeug.utils.secure_filename` bereinigt.

---

## 🚀 Lokales Setup & Installation

Folge diesen Schritten, um das Projekt lokal in einer Entwicklungsumgebung (z.B. mit XAMPP für MySQL) auszuführen.

### 1. Repository klonen
```bash
git clone https://github.com/Chris768356/OortCloud.git
cd OortCloud
```

### 2. Virtuelle Umgebung einrichten
```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
pip install pymysql cryptography
```

### 4. Umgebungsvariablen konfigurieren
Erstelle eine `.env`-Datei im Hauptverzeichnis und füge deine Datenbank-Credentials sowie den Flask Secret Key hinzu:
```env
SQLALCHEMY_DATABASE_URI=mysql+pymysql://DEIN_DB_USER:DEIN_DB_PASSWORT@localhost:3306/oortcloud
SECRET_KEY=dein_sehr_sicherer_geheimer_schluessel
UPLOAD_FOLDER=cloud_data/
```

### 5. Datenbank initialisieren & migrieren
*(Wichtig: Die Zieldatenbank `oortcloud` muss in deinem MySQL-Server bereits leer existieren)*
```bash
flask db init
flask db migrate -m "Initiale MySQL Migration"
flask db upgrade
```

### 6. Entwicklungsserver starten
```bash
flask run
```
Die Anwendung ist nun unter `http://127.0.0.1:5000` erreichbar.

---

## 📂 Projektstruktur (Auszug)

```text
OortCloud/
├── app/                    # Flask Application Factory & Blueprints
│   ├── auth.py             # Login, Registrierung, Session-Management
│   ├── dashboard.py        # Datei-Upload, Download, Löschung
│   ├── models.py           # SQLAlchemy Datenbank-Modelle (User, File)
│   ├── templates/          # Jinja2 HTML-Templates
│   └── static/             # CSS und SVG-Assets (OortCloud Logo)
├── migrations/             # Alembic Datenbank-Baupläne
├── .gitignore              # Ausschluss von .env, .venv, *.db, Upload-Ordnern
├── requirements.txt        # Python Abhängigkeiten
└── app.py                  # App-Entrypoint
```

---

## 👨‍💻 Autor
**Christopher Neumann**  
Angehender Fachinformatiker für Anwendungsentwicklung
