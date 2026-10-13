# OortCloud ☁️

OortCloud ist eine modulare, selbst gehostete Cloud-Speicher-Webanwendung auf Basis von Python (Flask) und MariaDB. Die Anwendung ist containerisiert, setzt auf das Application-Factory-Muster und bietet getrennte Konfigurationen für Produktion und lokale Entwicklung.

## 🚀 Features

* **Benutzerverwaltung & Authentifizierung:** Modulare Authentifizierung (`auth.py`) und Profilverwaltung (`profile.py`).
* **Dateiverwaltung & Uploads:** Persönliche Dateiablage mit dynamischer Ordnererstellung für Nutzer (`dashboard.py`, Just-in-Time Provisioning).
* **Admin-Panel:** Eigener Administrationsbereich (`admin.py`) zur Systemverwaltung.
* **Datenbank-Migrationen:** Schema-Versionierung via Flask-Migrate / Alembic.
* **Multi-Container-Setup:** Isolierte Container für Webserver und MariaDB-Datenbank.
* **Entwickler-Workflow:** Live-Reload und direkte Code-Spiegelung via `docker-compose.override.yml`.

## 🛠️ Tech Stack

* **Backend:** Python, Flask (Application Factory & Blueprints)
* **Datenbank & ORM:** MariaDB, SQLAlchemy, Flask-Migrate
* **WSGI / Webserver:** Gunicorn (Produktion), Flask Dev-Server (Entwicklung)
* **Containerisierung:** Docker, Docker Compose

## 📁 Projektstruktur

```text
oortcloud/
├── CloudApp/                   # Haupt-Anwendungspaket (Application Factory)
│   ├── models/                 # Datenbankmodelle
│   ├── routes/                 # Blueprints & Endpunkte
│   │   ├── admin.py            # Admin-Routen
│   │   ├── auth.py             # Login & Registrierung
│   │   ├── dashboard.py        # Dateiverwaltung & Uploads
│   │   └── profile.py          # Benutzereinstellungen
│   ├── services/               # Geschäftslogik & Helfer
│   │   ├── utils.py            # Hilfsfunktionen
│   │   └── validate.py         # Validierungslogik
│   ├── static/                 # Statische Dateien (CSS, JS, Assets)
│   ├── templates/              # Jinja2-HTML-Templates
│   ├── __init__.py             # Factory-Funktion (create_app)
│   ├── config.py               # Konfigurationsprofile
│   └── extensions.py           # Erweiterungen (db, migrate, login_manager)
├── instance/                   # Lokale Instanzdaten
├── migrations/                 # Alembic-/Flask-Migrate-Dateien
├── uploads/                    # Benutzerverzeichnisse & hochgeladene Dateien
├── .dockerignore               # Ausschlussdateien für den Docker-Build
├── .env.example                # Vorlage für Umgebungsvariablen
├── .gitignore                  # Git-Ausschlussregeln
├── app.py                      # Einstiegspunkt zum Starten der Anwendung
├── Dockerfile                  # Produktions-Image (mit Gunicorn)
├── docker-compose.yml          # Basis-Dienste (Flask App & MariaDB)
├── docker-compose.override.yml # Lokale Dev-Erweiterung (Bind-Mount, FLASK_DEBUG)
├── README.md                   # Projektdokumentation
└── requirements.txt            # Python-Abhängigkeiten
```

## ⚙️ Voraussetzungen

* [Docker Engine](https://docs.docker.com/engine/install/) (Version 24.x oder neuer)
* [Docker Compose](https://docs.docker.com/compose/) (V2)
* Git

## 🚦 Schnellstart

### 1. Repository klonen

```bash
git clone https://github.com/dein-nutzername/oortcloud.git
cd oortcloud
```

### 2. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei anhand der Vorlage:

```bash
cp .env.example .env
```

Passe die Werte in `.env` an:

```env
DB_ROOT_PASSWORD=dein_geheimes_root_passwort
DB_PASSWORD=dein_datenbank_passwort
UPLOAD_FOLDER=/app/uploads
SECRET_KEY=ein_zufaelliger_geheimer_schluessel
```

### 3. Container starten

```bash
docker compose up -d --build
```

Die Anwendung ist im Browser unter `http://localhost:5000` erreichbar.

## 💻 Entwicklungsumgebung (Dev-Mode)

Für die lokale Entwicklung wird die `docker-compose.override.yml` genutzt. Sie bindet das Arbeitsverzeichnis per Bind-Mount ein und aktiviert den Hot-Reload:

```yaml
services:
  web:
    command: flask run --host=0.0.0.0
    volumes:
      - .:/app
    environment:
      FLASK_DEBUG: "1"
```

Änderungen in `CloudApp/`, in den Templates oder Routen werden damit sofort aktiv, ohne die Container neu zu bauen.

### Nützliche Befehle

* **Logs einsehen:**
  ```bash
  docker compose logs -f web
  ```

* **Datenbank-Migrationen ausführen:**
  ```bash
  docker compose exec web flask db upgrade
  ```

* **Datenbank-Shell öffnen:**
  ```bash
  docker compose exec db mariadb -u oortcloud_user -p oortcloud_db
  ```

* **Container stoppen:**
  ```bash
  docker compose down
  ```

## 🗺️ Roadmap

- [ ] Vollständige OOP-Kapselung der Dateiverwaltung (`StorageManager`-Klasse)
- [ ] Umstellung ausgewählter Endpunkte auf Klassenbasierte Views (`MethodView`)
- [ ] Speicherquoten pro Benutzer
- [ ] Freigabe-Links mit Ablaufdatum

## 📄 Lizenz

Dieses Projekt ist unter der [MIT License](LICENSE) lizenziert.