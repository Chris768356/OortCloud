from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from CloudApp.extensions import db, limiter
from CloudApp.models.user import User

profile_bp = Blueprint("profile", __name__)

@profile_bp.route("/")
@login_required
def show_profile():
    return render_template("profile.html")

@profile_bp.route("/change_username", methods = ["POST"])
@login_required
def change_username():
    new_username = request.form.get("new_username")
    