from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core
# Added import for cohort_users join table
from cwmt.models.teams import team_members

db = core.app.db
app = core.app
bcrypt = core.app.bcrypt

# -------------------------
# Users Has Roles Table
# -------------------------
user_roles = db.Table('user_roles',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)   

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

    
    # RELATIONSHIPS
    roles = db.relationship('Role', secondary=user_roles, lazy='subquery', backref=db.backref('users', lazy=True))
    teams = db.relationship('Team', secondary=team_members, lazy='subquery', backref=db.backref('users', lazy=True))

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
    def validate_login(data:dict):
        is_valid = True

        print(core.show_attributes())

        if not data.get('email'):
            is_valid = False
            core.logger.log('Email is required.', with_flash=True, status='error')
        if not data.get('password'):
            is_valid = False
            core.logger.log('Password is required.', with_flash=True, status='error')

        user = User.query.filter_by(email=data.get('email')).first()
        if not user:
            is_valid = False
            core.logger.log('User not found.', with_flash=True, status='error')

        if user and not bcrypt.check_password_hash(user.password, data.get('password')):
            is_valid = False
            core.logger.log('Invalid password.', with_flash=True, status='error')

        if is_valid:
            return user
        return is_valid

        
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
