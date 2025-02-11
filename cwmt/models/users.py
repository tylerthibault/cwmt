from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import AppCore
# Added import for cohort_users join table
from cwmt.models.cohorts import cohort_users

db = AppCore.app.db
bcrypt = AppCore.app.bcrypt

# -------------------------
# Users Table
# -------------------------
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    has_verified_email = db.Column(db.Boolean, default=False)

    
    # Many-to-Many with roles via a join table.
    roles = db.relationship('Roles', secondary='user_roles', back_populates='users', lazy='dynamic')
    # Many-to-Many with teams.
    teams = db.relationship('Team', secondary='team_members', back_populates='members', lazy='dynamic')
    # Updated relationship: using imported cohort_users join table object.
    cohorts = db.relationship('Cohort', secondary=cohort_users, back_populates='participants', lazy='dynamic')

    @classmethod
    def create(cls, data:dict):
        validate_data = cls.validate(data)
        if not validate_data:
            return None
        
        data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'password': bcrypt.generate_password_hash(data.get('password')).decode('utf-8'),
            'is_active': data.get('is_active', True),
            'has_verified_email': data.get('has_verified_email', False)
        }
        user = cls(**data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def get(cls, user_id:int):
        return cls.query.get(user_id)
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def update(cls, user_id:int, data:dict):
        user = cls.query.get(user_id)
        for key, value in data.items():
            if hasattr(user, key):
                if key == 'password':
                    value = bcrypt.generate_password_hash(value).decode('utf-8')
                if key == 'email':
                    user.has_verified_email = False
            setattr(user, key, value)
        db.session.commit()
        return user
    
    @classmethod
    def delete(cls, user_id:int):
        user = cls.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        return user
    
    @staticmethod
    def validate(data:dict):
        is_valid = True
        if not data.get('first_name'):
            is_valid = False
            app.core.logger.log('First name is required.', with_flash=True, status='error')
        if not data.get('last_name'):
            is_valid = False
            app.core.logger.log('Last name is required.', with_flash=True, status='error')
        if not data.get('email'):
            is_valid = False
            app.core.logger.log('Email is required.', with_flash=True, status='error')
        if not data.get('password'):
            is_valid = False
            app.core.logger.log('Password is required.', with_flash=True, status='error')
        return is_valid
