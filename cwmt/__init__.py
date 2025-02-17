from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from cwmt.helpers.app_core.core import AppCore

core = AppCore()

def create_app():
    app = Flask(__name__)

    core.app = app
    app.bcrypt = Bcrypt(app)
    app.secret_key = 'supersecretkey'

    init_db(app)
    init_blueprints(app)


    return app


def init_blueprints(app):
    from cwmt.controllers.routes import main_bp
    app.register_blueprint(main_bp)

    from cwmt.controllers.users import users_bp
    app.register_blueprint(users_bp)

    from cwmt.controllers.teams import teams_bp
    app.register_blueprint(teams_bp)

    from cwmt.controllers.cohorts import cohorts_bp
    app.register_blueprint(cohorts_bp)

    from cwmt.controllers.locations import locations_bp
    app.register_blueprint(locations_bp)

    from cwmt.controllers.templates import templates_bp
    app.register_blueprint(templates_bp)

    from cwmt.controllers.base_crud_routes import base_routes_db
    app.register_blueprint(base_routes_db)

    # from cwmt.controllers.instructors import instructors_bp
    # app.register_blueprint(instructors_bp)

    return app

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cwmt.db'
    app.db = SQLAlchemy(app)

    from cwmt.models.roles import Role
    from cwmt.models.users import User, user_roles
    from cwmt.models.teams import Team, team_members
    from cwmt.models.cohorts import Cohort, cohort_students, cohort_locations, cohort_instructors
    from cwmt.models.locations import Location
    from cwmt.models.templates import Template, template_cohort_locations

    with app.app_context():
        app.db.create_all()
    
    return app

app = create_app()