from flask import Blueprint, render_template, request, flash, url_for, redirect
from market import db
from market.forms import PurchaseItemForm, ReturnItemForm
from market.models import Item
from flask_login import login_required, current_user


markets = Blueprint("markets", __name__)


@markets.route("/market", methods=["GET", "POST"])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    returning_form = ReturnItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get("purchased_item")
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                current_user.purchase_item(p_item_obj)
                db.session.commit()
                flash(f"Congratulations! You purchased {p_item_obj.name} for ${p_item_obj.price}", category="success")
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_obj.name}", category="danger")

        # Return Item Logic
        returned_item = request.form.get("returned_item")
        r_item_obj = Item.query.filter_by(name=returned_item).first()
        if r_item_obj:
            if current_user.can_return(r_item_obj):
                current_user.return_item(r_item_obj)
                db.session.commit()
                flash(f"Congratulations! You returned {r_item_obj.name} back to Market!", category="success")
            else:
                flash(f"Something went wrong with returning {r_item_obj.name}", category="danger")

        return redirect(url_for("markets.market"))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template("market.html", items=items, purchase_form=purchase_form, owned_items=owned_items, returning_form=returning_form)
