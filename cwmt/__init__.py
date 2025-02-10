from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)

    app.bcrypt = Bcrypt(app)

    init_blueprints(app)
    init_db(app)


    return app


def init_blueprints(app):
    from cwmt.controllers.routes import main
    app.register_blueprint(main)



    return app

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cwmt.db'
    app.db = SQLAlchemy(app)
    
    return app