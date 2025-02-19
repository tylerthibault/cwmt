from datetime import datetime
import uuid
import hashlib
from sqlalchemy import Column, Integer, String, DateTime

from cwmt import core
app = core.app
db = app.db

class LogBook(db.Model):
    __tablename__ = 'logbooks'  # Name of the table in the database

    id = Column(Integer, primary_key=True)  # Unique identifier for each log entry
    user_id = Column(Integer, nullable=False)  # ID of the user who performed the login
    first_name = Column(String(64), nullable=False)  # first name of the user
    last_name = Column(String(64), nullable=False)  # last name of the user
    ip_address = Column(String(45), nullable=True)  # IP address from where the login was made
    user_agent = Column(String(255), nullable=True)  # User agent string of the client
    login_time = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the login occurred
    user_role = Column(String(255), nullable=True)  # Role of the user who performed the login
    session_token = Column(String(64), nullable=False)  # Unique token assigned to the session

    created_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of when the log entry was created
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Timestamp of the last update

    def __init__(self, user_id, first_name, last_name, user_role, ip_address=None, user_agent=None):
        # Initialize a login record with provided user information and generate a session token
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.ip_address = ip_address
        self.user_role = user_role
        self.user_agent = user_agent
        self.session_token = self.generate_session_token()

    @classmethod
    def create(cls, data: dict):
        """
        Create a new login log entry with the provided data.
        data: A dictionary containing the user information and optional IP address and user agent.
        """
        # Create a new log entry with the provided data
        data = {
            'user_id': data.get('user_id'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'ip_address': data.get('ip_address'),
            'user_role': data.get('user_role'),
            'user_agent': data.get('user_agent'),
        }
        log_entry = cls(**data)
        db.session.add(log_entry)
        db.session.commit()

        return log_entry.session_token

    @classmethod
    def update_timestamp(cls, session_token):
        """
        Update the timestamp of the login log entry with the provided session token.
        session_token: The session token of the login log entry to update.
        """
        # Find the log entry with the provided session token and update its timestamp
        log_entry = cls.query.filter_by(session_token=session_token).first()
        if log_entry:
            log_entry.updated_at = datetime.utcnow()
            db.session.commit()
            

    @classmethod
    def check_timestamp(cls, session_token, max_age=3600):
        """
        Check if the login log entry with the provided session token is within the maximum age.
        session_token: The session token of the login log entry to check.
        max_age: The maximum age in seconds for the login log entry (default: 1 hour).
        """
        # Find the log entry with the provided session token and check its timestamp
        log_entry = cls.query.filter_by(session_token=session_token).first()
        if log_entry:
            current_time = datetime.utcnow()
            if (current_time - log_entry.updated_at).total_seconds() <= max_age:
                core.logger.log('Session token is valid.', with_flash=False, status='info')
                return log_entry
        core.logger.log('Session token failed timeout.', with_flash=False, status='error')
        return False

    @staticmethod
    def generate_session_token():
        """Generate a unique session token using UUID and SHA-256"""
        random_uuid = str(uuid.uuid4())  # Create a random UUID string
        return hashlib.sha256(random_uuid.encode()).hexdigest()  # Return its SHA-256 hash

    def __repr__(self):
        # Provide a string representation of the login log entry
        return f'<LoginLog {self.username} - {self.login_time}>'