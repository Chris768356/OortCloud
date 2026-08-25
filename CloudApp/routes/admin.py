from flask import Blueprint, render_template, request, url_for, redirect, current_app
from flask_login import login_required, current_user
from CloudApp.services.utils import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
@login_required
@admin_required
def admin_dashboard():
    pass