from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import logging
from logging.handlers import RotatingFileHandler
import os


db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = "super secret key"


    bcrypt.init_app(app)

    # Setup logging
    setup_logging(app)

    # setup the db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)

    setup_tables(app)
    register_blueprints(app)

    return app

def register_blueprints(app):
    # register the blueprints
    from cwmt.controllers.routes import routes_bp
    app.register_blueprint(routes_bp)

    from cwmt.controllers.users import users_bp
    app.register_blueprint(users_bp)

    from cwmt.controllers.instructors import instructors_bp
    app.register_blueprint(instructors_bp)

    from cwmt.controllers.courses import courses_bp, course_sessions_bp
    app.register_blueprint(courses_bp)
    app.register_blueprint(course_sessions_bp)

    # from cwmt.controllers.students import students_bp
    # app.register_blueprint(students_bp)

    # from cwmt.controllers.course_sessions import course_sessions_bp
    # app.register_blueprint(course_sessions_bp)

    # from cwmt.controllers.enrollments import enrollments_bp
    # app.register_blueprint(enrollments_bp)

    # from cwmt.controllers.locations import locations_bp
    # app.register_blueprint(locations_bp)
    

def setup_tables(app):
    # from cwmt.models import User
    from cwmt.models.log import Log
    from cwmt.models.users import User
    from cwmt.models.instructors import Instructor
    from cwmt.models.teams import Team
    from cwmt.models.roles import Role, UserRole
    from cwmt.models.courses import Course
    with app.app_context():
        db.create_all()


def setup_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Admin logger setup
    admin_handler = RotatingFileHandler(
        'logs/admin.log',
        maxBytes=10240,
        backupCount=5
    )
    admin_handler.setFormatter(logging.Formatter(
        '[ADMIN] %(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    admin_handler.setLevel(logging.INFO)
    
    admin_logger = logging.getLogger('admin')
    admin_logger.addHandler(admin_handler)

    # CHANGE THIS TO SET THE LOGGING LEVEL FOR THE ADMIN LOGGER
    # admin_logger.setLevel(logging.DEBUG)
    admin_logger.setLevel(logging.INFO)
    # admin_logger.setLevel(logging.WARNING)
    # admin_logger.setLevel(logging.ERROR)
    # admin_logger.setLevel(logging.CRITICAL)
    
    # User activity logger setup
    user_handler = RotatingFileHandler(
        'logs/user_activity.log',
        maxBytes=10240,
        backupCount=5
    )
    user_handler.setFormatter(logging.Formatter(
        '[USER] %(asctime)s: %(message)s'
    ))
    user_handler.setLevel(logging.INFO)
    
    user_logger = logging.getLogger('user_activity')
    user_logger.addHandler(user_handler)

    # CHANGE THIS TO SET THE LOGGING LEVEL FOR THE USER ACTIVITY LOGGER
    # user_logger.setLevel(logging.DEBUG)
    user_logger.setLevel(logging.INFO)
    # user_logger.setLevel(logging.WARNING)
    # user_logger.setLevel(logging.ERROR)
    # user_logger.setLevel(logging.CRITICAL)
    
    # Console handler for development
    console_handler = logging.StreamHandler()

    # CHANGE THIS TO SET THE LOGGING LEVEL FOR THE CONSOLE
    # console_handler.setLevel(logging.DEBUG)
    console_handler.setLevel(logging.INFO)
    # console_handler.setLevel(logging.WARNING)
    # console_handler.setLevel(logging.ERROR)
    # console_handler.setLevel(logging.CRITICAL)


    console_handler.setFormatter(logging.Formatter(
        '%(name)s - %(levelname)s: %(message)s'
    ))
    
    # Add console handler to both loggers
    admin_logger.addHandler(console_handler)
    user_logger.addHandler(console_handler)
    
    # Store loggers in app config for easy access
    app.config['admin_logger'] = admin_logger
    app.config['user_logger'] = user_logger
    
    admin_logger.info('Admin logging started')
    user_logger.info('User activity logging started')

    # app.logger.setLevel(logging.DEBUG)
    # app.logger.setLevel(logging.INFO)
    # app.logger.setLevel(logging.WARNING)
    # app.logger.setLevel(logging.ERROR)
    # app.logger.setLevel(logging.CRITICAL)
    

                