from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret key"

    bcrypt.init_app(app)

    # setup the db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    # from management.models import User
    from management.models.log import Log
    from management.models.users import User
    with app.app_context():
        db.create_all()

    # register the blueprints
    from management.controllers.routes import routes_bp
    app.register_blueprint(routes_bp)

    from management.controllers.users import users_bp
    app.register_blueprint(users_bp)

    return app