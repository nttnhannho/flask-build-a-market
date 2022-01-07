from flask import Blueprint, render_template, request, flash
from market import db
from market.forms import PurchaseItemForm
from market.models import Item
from flask_login import login_required, current_user


markets = Blueprint("markets", __name__)


@markets.route("/market", methods=["GET", "POST"])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    if request.method == "POST":
        purchase_item = request.form.get("purchase_item")
        p_item_obj = Item.query.filter_by(name=purchase_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                current_user.purchase(p_item_obj)
                db.session.commit()
                flash(f"Congratulations! You purchased {p_item_obj.name} for ${p_item_obj.price}", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_obj.name}", category="danger")
    items = Item.query.filter_by(owner=None)
    return render_template("market.html", items=items, purchase_form=purchase_form)
