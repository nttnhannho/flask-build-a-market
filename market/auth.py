from flask import Blueprint, render_template, redirect, url_for
from market import db
from market.forms import RegisterForm
from market.models import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for("views.market_page"))
    if form.errors:
        for err_msg in form.errors.values():
            print(f"There was an error with creating a user: {err_msg}")
    return render_template("register.html", form=form)
