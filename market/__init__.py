from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


DATABASE_NAME = "market.db"
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "f33c9a2b156a0065e2c635e1863d799edf3d669943606de91beac3a2c400a307"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)

    from market.views import views
    from market.auths import auths
    from market.markets import markets
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auths, url_prefix="/")
    app.register_blueprint(markets, url_prefix="/")

    from market.models import Item
    create_database(app)

    login_manager.init_app(app)
    login_manager.login_view = "auths.login"
    login_manager.login_message_category = "info"

    return app


def create_database(app):
    if not Path(f"market/{DATABASE_NAME}").exists():
        with app.app_context():
            db.create_all(app=app)
            print("Database created!!!")
