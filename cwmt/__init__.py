from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cwmt.helpers.app_core.core import AppCore

from flask_bcrypt import Bcrypt


def create_app():
    app = Flask(__name__)

    app.bcrypt = Bcrypt(app)

    init_blueprints(app)
    init_db(app)

    app.core = AppCore()

    return app


def init_blueprints(app):
    from cwmt.controllers.routes import main_bp
    app.register_blueprint(main_bp)

    from cwmt.controllers.users import users_bp
    app.register_blueprint(users_bp)

    return app

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cwmt.db'
    app.db = SQLAlchemy(app)
    
    return app

app = create_app()