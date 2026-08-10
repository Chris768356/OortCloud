import os
from flask import Flask , render_template, flash, redirect , url_for, request
from werkzeug.exceptions import RequestEntityTooLarge
from CloudApp.extensions import db, csrf, login_manager, limiter, migrate
from flask_wtf.csrf import CSRFError



def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=False)
    else:
        app.config.from_mapping(test_config)
    
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    migrate.init_app(app, db)

    os.makedirs(app.instance_path, exist_ok=True)
    


    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' 'unsafe-inline';"

        # Erst aktivieren, wenn Server wirklich ein SSL-Zertifikat hat!
        # HSTS (Strict-Transport-Security): Zwingt den Browser, für 1 Jahr nur noch HTTPS zu nutzen
        # response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        return response

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    @app.errorhandler(413)
    def handle_too_large_error(error):
        flash("Die Datei ist zu groß für den Server!", "error")
        return redirect(url_for("dashboard.dashboard"))

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        flash("Deine Sitzung ist abgelaufen oder ungültig. Bitte versuche es erneut.", "error")
        return redirect(request.referrer or url_for("auth.login"))
    

    @app.route("/")
    def index():
        return render_template("index.html")
    
    @app.route("/agb")
    def agb():
        return render_template("agb.html")
    
    @app.route("/dsgvo")
    def dsgvo():
        return render_template("dsgvo.html")

    from CloudApp.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    from CloudApp.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp, url_prefix = "/dashboard")

    from CloudApp.models.user import User
    from CloudApp.models.file import File

    return app

