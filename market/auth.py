from flask import Blueprint, render_template, redirect, url_for, flash
from market import db
from market.forms import RegisterForm
from market.models import User
from werkzeug.security import generate_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=generate_password_hash(form.password.data, method="sha256"))
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("views.market"))
    if form.errors:
        for err_msg in form.errors.values():
            flash(f"{err_msg}", category="danger")
    return render_template("register.html", form=form)
