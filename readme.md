# OortCloud ☁️

OortCloud ist eine leichtgewichtige, selbst gehostete Cloud-Speicher-Webanwendung auf Basis von Python (Flask) und MariaDB. Die Anwendung ist vollständig containerisiert und bietet sowohl eine produktionsreife Basis als auch ein flexibles Setup für die lokale Entwicklung.

---

## 🚀 Features

- **Benutzerverwaltung:** Sichere Registrierung und Authentifizierung von Benutzern.
- **Dateiverwaltung & Uploads:** Persönliche Dateiablage mit dynamischer Erstellung benutzerspezifischer Speicherordner (*Just-in-Time Provisioning*).
- **Persistente Datenhaltung:** Vollständige Trennung von Anwendungslogik und Datenbankdaten über Docker-Volumes.
- **Docker-native Architektur:** Multi-Container-Setup für Webserver und Datenbank.
- **Entwickler-Workflow:** Unterstützung für Live-Reload und Bind-Mounts via Docker Compose Override.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **WSGI / Webserver:** Gunicorn (Produktion), Flask Dev-Server (Entwicklung)
- **Datenbank:** MariaDB
- **Containerisierung:** Docker, Docker Compose

---

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
├── README.md                   # Projektdokumentation
└── requirements.txt            # Python-Abhängigkeiten
```
---

## ⚙️ Voraussetzungen

- [Docker Engine](https://docs.docker.com/engine/install/) (Version 24.x oder neuer)
- [Docker Compose](https://docs.docker.com/compose/) (V2)
- Git

---

## 🚦 Schnellstart

### 1. Repository klonen

```bash
git clone https://github.com/Chris768356/OortCloud.git
cd oortcloud
```

### 2. Umgebungsvariablen konfigurieren

Erstelle eine `.env`-Datei auf Basis der Vorlage:

```bash
cp .env.example .env
```

Passe die Variablen in `.env` an deine lokalen Einstellungen an:

```ini
DB_ROOT_PASSWORD=dein_geheimes_root_passwort
DB_PASSWORD=dein_datenbank_passwort
UPLOAD_FOLDER=/app/uploads
SECRET_KEY=ein_zufaelliger_geheimer_schluessel
```

### 3. Container starten

```bash
docker compose up -d --build
```

Die Anwendung ist anschließend im Browser unter `http://localhost:5000` erreichbar.

---


### Nützliche Befehle

- **Logs einsehen:**
  ```bash
  docker compose logs -f web
  ```
- **Container stoppen:**
  ```bash
  docker compose down
  ```
- **Datenbank-Shell öffnen:**
  ```bash
  docker compose exec db mariadb -u oortcloud_user -p oortcloud_db
  ```

---

## 🗺️ Roadmap

- [ ] Refactoring zu einer modularen, objektorientierten Architektur (OOP)
- [ ] Implementierung von Service-Klassen (`StorageManager`, `UserManager`)
- [ ] Klassenbasierte Views (`Flask MethodView`)
- [ ] Freigabe-Links und Berechtigungsmanagement für Dateien


