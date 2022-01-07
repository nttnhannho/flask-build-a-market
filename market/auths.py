from flask import Blueprint, render_template, redirect, url_for, flash
from market import db
from market.forms import RegisterForm, LoginForm
from market.models import User
from flask_login import login_user, logout_user


auths = Blueprint("auths", __name__)


@auths.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for("markets.market"))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f"{err_msg}", category="danger")
    return render_template("register.html", form=form)


@auths.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f"Success! You are logged in as {attempted_user.username}", category="success")
            return redirect(url_for("markets.market"))
        else:
            flash(f"Incorrect user name or password! Please try again.", category="danger")
    return render_template("login.html", form=form)


@auths.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!", category="info")
    return redirect(url_for("views.home"))
