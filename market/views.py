from flask import render_template, Blueprint
from market.models import Item


views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html")


@views.route("/market")
def market():
    items = Item.query.all()
    return render_template("market.html", items=items)
