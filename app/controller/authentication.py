from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash
from ..model.user import User
from ..utils.forms import LoginForm

authentication = Blueprint("authentication", __name__)


@authentication.route("/login", methods=["GET", "POST"])
def login():
    forms = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for("admin.index"))

    if request.method == "POST" and forms.validate_on_submit():
        user = User.query.filter_by(username=forms.username.data).first()
        if user:
            if check_password_hash(user.password, forms.password.data):
                login_user(user)

                if current_user.role == "admin":
                    return redirect(url_for("admin.index"))

                return redirect(url_for("student.index"))

            else:
                flash("Invalid password", category="danger")
                return redirect(url_for("authentication.login"))
        else:
            flash("Username tidak ditemukan", category="danger")
            return redirect(url_for("authentication.login"))

    return render_template("login.html", forms=forms)


@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("authentication.login"))
