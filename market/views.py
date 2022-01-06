from flask import render_template, Blueprint
from market.models import Item
from flask_login import login_required


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/market")
@login_required
def market():
    items = Item.query.all()
    return render_template("market.html", items=items)
