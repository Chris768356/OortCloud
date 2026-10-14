# OortCloud ☁️

![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20development-success)


OortCloud ist eine leichtgewichtige, selbst gehostete Cloud-Speicher-Webanwendung auf Basis von Python (Flask) und MariaDB. Die Anwendung folgt einer sauberen Service-Layer-Architektur, ist vollständig containerisiert und bietet sowohl eine produktionsreife Basis als auch ein flexibles Setup für die lokale Entwicklung.

---
> **Hinweis:** Dies ist ein Portfolio-Projekt zur Demonstration von Backend-Architektur, sicherem Datei-Handling und relationaler Datenbankmodellierung.
## 🚀 Features

- **Mehrschichtige Architektur (Service Layer & DTOs):** Saubere Trennung zwischen HTTP-Routing (Blueprints), Dateisystem-Logik (`StorageService` auf Basis von `pathlib`) und Datenhaltung (`SQLAlchemy`), entkoppelt über Data Transfer Objects (`StoredFileDTO`).
- **Security & Dateisystem-Isolation:** Schutz vor Path-Traversal und ID-Enumeration durch UUID-basierte Benutzerverzeichnisse (`directory_uuid`), verschleierte Dateinamen auf dem Speichermedium, Dateityp-Validierung sowie Rate-Limiting (`Flask-Limiter`).
- **Transaktionssicherheit & Quotas:** Individuelle Speicherplatzkontingente (`USER_QUOTA`) pro Benutzer sowie atomare Operationen mit automatischem Datenbank-Rollback und Dateisystem-Cleanup im Fehlerfall.
- **Just-in-Time Provisioning:** Persönliche Speicherordner werden ressourcenschonend erst beim ersten tatsächlichen Datei-Upload angelegt.
- **Persistente Datenhaltung:** Vollständige Trennung von Anwendungslogik, hochgeladenen Dateien und Datenbankdaten über Docker-Volumes.
- **Docker-native Architektur:** Multi-Container-Setup für Webserver (Gunicorn) und Datenbank (MariaDB) inklusive Entwickler-Workflow mit Live-Reload.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask, SQLAlchemy, Flask-Login, Flask-Limiter, Flask-Migrate
- **WSGI / Webserver:** Gunicorn (Produktion), Flask Dev-Server (Entwicklung)
- **Datenbank:** MariaDB
- **Containerisierung:** Docker, Docker Compose

---

## 📁 Projektstruktur

```text
oortcloud/
├── CloudApp/                   # Haupt-Anwendungspaket (Application Factory)
│   ├── dto/                    # Data Transfer Objects
│   │   └── file_dto.py         # DTO für Datei-Metadaten (StoredFileDTO)
│   ├── models/                 # SQLAlchemy Datenbankmodelle
│   │   ├── file.py             # Datei-Modell
│   │   └── user.py             # Benutzer-Modell
│   ├── routes/                 # Blueprints & HTTP-Endpunkte (Controller)
│   │   ├── admin.py            # Admin-Routen
│   │   ├── auth.py             # Login & Registrierung
│   │   ├── dashboard.py        # Dateiverwaltung, Uploads & Downloads
│   │   └── profile.py          # Benutzereinstellungen
│   ├── services/               # Gekapselte Geschäfts- & Dateisystemlogik
│   │   ├── storage.py          # StorageService (pathlib Dateisystem-Management)
│   │   ├── utils.py            # Hilfsfunktionen
│   │   └── validate.py         # Validierungslogik
│   ├── static/                 # Statische Dateien (CSS, JS, Assets)
│   ├── templates/              # Jinja2-HTML-Templates
│   ├── __init__.py             # Factory-Funktion (create_app)
│   ├── config.py               # Konfigurationsprofile
│   └── extensions.py           # Erweiterungen (db, migrate, login_manager, limiter)
├── instance/                   # Lokale Instanzdaten
├── migrations/                 # Alembic-/Flask-Migrate-Dateien
├── uploads/                    # Isolierte Benutzerverzeichnisse & Dateien
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
BASE_UPLOAD_FOLDER=/app/uploads
SECRET_KEY=ein_zufaelliger_geheimer_schluessel
```

### 3. Container starten

```bash
docker compose up -d --build
```

### 4. Datenbank-Tabellen initialisieren

Beim ersten Start mit einem neuen Datenbank-Volume müssen die Tabellen angelegt werden:

```bash
docker compose exec web flask db upgrade
```

Die Anwendung ist anschließend im Browser unter `http://localhost:5000` erreichbar.

---

## 🔧 Nützliche Befehle

- **Logs der Web-App einsehen:**
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

- [x] Refactoring zu einer modularen, objektorientierten Architektur (Service Layer & DTOs)
- [x] Implementierung des `StorageService` für isolierte Dateisystem-Operationen
- [ ] Ausbau weiterer Service-Klassen (z. B. `UserService` / `AuthService`)
- [ ] Klassenbasierte Views (`Flask MethodView`)
- [ ] Freigabe-Links und Berechtigungsmanagement für Dateien


