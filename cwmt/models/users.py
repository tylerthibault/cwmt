from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from cwmt.models.teams import Team

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    roles = db.relationship('UserRole', backref='user', lazy=True)
    teams = db.relationship('Team', backref='owner', lazy=True)
    # instructor_profile = db.relationship('Instructor', backref='user', uselist=False, lazy=True)  # One-to-one for instructor profile if applicable

    @classmethod
    def create(cls, data:dict):
        """
        Create a new user record in the database

        args data: dict: A dictionary containing the user's data
        dict: username, email, password

        returns User: A User object
        """
        try:
            data = {**data}
            data['password'] = cls.hash_password(data['password'])
            user = cls(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            flash(f"Error creating user: {e}", 'error')
            return None
    
    @staticmethod
    def hash_password(password:str):
        """
        Hash a password using bcrypt

        args password: str: The password to hash

        returns str: The hashed password
        """
        return bcrypt.generate_password_hash(password).decode('utf-8')
    
    
    @staticmethod
    def validate_login(data:dict):
        """
        Validate a user's login credentials

        args data: dict: A dictionary containing the user's login data
        dict: username, password

        returns User: A User object if successful, else None
        """
        user = User.query.filter_by(username=data['username']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            print("checked password")
            return user
        
        print('Invalid login credentials')
        flash('Invalid login credentials', 'error')
        return None