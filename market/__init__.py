from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
DATABASE_NAME = "market.db"

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "f33c9a2b156a0065e2c635e1863d799edf3d669943606de91beac3a2c400a307"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)

    from market.views import views
    from market.auth import auth
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from market.models import Item
    create_database(app)

    return app


def create_database(app):
    if not Path(f"market/{DATABASE_NAME}").exists():
        with app.app_context():
            db.create_all(app=app)
            print("Database created!!!")
