from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from cwmt.helpers.app_core.core import AppCore


def create_app():
    app = Flask(__name__)

    AppCore.app = app
    app.bcrypt = Bcrypt(app)

    init_db(app)
    init_blueprints(app)


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