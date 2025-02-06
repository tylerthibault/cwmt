import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from logging.handlers import RotatingFileHandler
from sqlalchemy.exc import OperationalError

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    
    # Application Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Setup database tables and logging
    setup_tables(app)
    setup_logging(app)
    
    # Register Blueprints (uncomment and modify as required)
    # from cwmt.controllers.students import students_bp
    # app.register_blueprint(students_bp)
    # from cwmt.controllers.course_sessions import course_sessions_bp
    # app.register_blueprint(course_sessions_bp)
    # from cwmt.controllers.enrollments import enrollments_bp
    # app.register_blueprint(enrollments_bp)
    # from cwmt.controllers.locations import locations_bp
    # app.register_blueprint(locations_bp)
    
    # Added test endpoint to verify server response
    @app.route("/status")
    def status():
        return "Server is running", 200
    
    return app

def setup_tables(app):
    with app.app_context():
        # Import models here to avoid circular imports
        from cwmt.models.log import Log
        from cwmt.models.users import User  # added import to resolve foreign key reference
        # import other models as needed, e.g.:
        # from cwmt.models.users import User
        # from cwmt.models.instructors import Instructor
        # from cwmt.models.teams import Team
        # from cwmt.models.roles import Role, UserRole
        # from cwmt.models.courses import Course
        try:
            db.create_all()
        except OperationalError:
            print("Tables already exist, skipping creation.")

def setup_logging(app):
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    # Set up an admin logger
    admin_handler = RotatingFileHandler(
        'logs/admin.log',
        maxBytes=10240,
        backupCount=5
    )
    admin_handler.setLevel('INFO')
    app.logger.addHandler(admin_handler)
    
    # Set up additional logging for user activity
    user_activity_handler = RotatingFileHandler(
        'logs/user_activity.log',
        maxBytes=10240,
        backupCount=5
    )
    user_activity_handler.setLevel('INFO')
    app.logger.addHandler(user_activity_handler)

# Expose the app callable for WSGI servers
app = create_app()

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)