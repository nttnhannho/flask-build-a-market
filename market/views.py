from flask import render_template, Blueprint
from market.models import Item
from market.forms import RegisterForm


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home_page():
    return render_template("home.html")


@views.route("/market")
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@views.route("/register")
def register_page():
    form = RegisterForm()
    return render_template("register.html", form=form)
