from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core
# Added import for cohort_users join table
from cwmt.models.teams import team_members
from cwmt.models import roles

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

    @property
    def show_roles(self):
        return ', '.join([role.name for role in self.roles])
    
    @property
    def name(self):
        return f'{self.first_name.capitalize()} {self.last_name.capitalize()}'

    @classmethod
    def create(cls, data:dict):
        validate_data = cls.validate(data)
        if not validate_data:
            core.logger.log('User creation failed.', with_flash=True, status='error')
            return None
        
        try:
            if data.get('submit-type') == 'admin':
                data['password'] = data['first_name'] + '.' + data['last_name']

            user_data = {
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'email': data.get('email'),
                'password': bcrypt.generate_password_hash(data.get('password')).decode('utf-8'),
                'is_active': data.get('is_active', True),
                'has_verified_email': data.get('has_verified_email', False)
            }

            user = cls(**user_data)

            print("*"*80)
            print(data)
            if data.get('role_id'):
                print("*"*80)
                role = roles.Role.get_by_id(data.get('role_id'))
                print(role)
                if role:
                    user.roles.append(role)

            db.session.add(user)
            db.session.commit()
            core.logger.log(f'User {user.first_name} {user.last_name} created.', with_flash=True, flash_category='success')
            return user
        
        except Exception as e:
            db.session.rollback()
            core.logger.log(f'Error creating user: {e}', with_flash=True, status='error')
    
    @classmethod
    def get(cls, user_id:int):
        return cls.query.get(user_id)
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def update(cls, user_id:int, data:dict):
        user = cls.query.get(user_id)
        if not user:
            core.logger.log(f'User with ID {user_id} not found.', with_flash=True, status='error')
            return None
        
        print("#"*80)
        for key, value in data.items():
            print(f"key: {key}, value: {value}")
            if hasattr(user, key):
                if key == 'password':
                    value = bcrypt.generate_password_hash(value).decode('utf-8')
                if key == 'email':
                    user.has_verified_email = False
            setattr(user, key, value)
        
        db.session.commit()
        core.logger.log(f'User {user.first_name} updated.', with_flash=True, flash_category='success')
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
            core.logger.log('First name is required.', with_flash=True, status='error')
        
        if not data.get('last_name'):
            is_valid = False
            core.logger.log('Last name is required.', with_flash=True, status='error')
        
        if not data.get('email'):
            is_valid = False
            core.logger.log('Email is required.', with_flash=True, status='error')

        existing_user = User.query.filter_by(email=data.get('email')).first()
        if existing_user:
            is_valid = False
            core.logger.log('Email already exists.', with_flash=True, status='error')

        if data.get('submit-type') != 'admin':
            if not data.get('password'):
                is_valid = False
                core.logger.log('Password is required.', with_flash=True, status='error')
        return is_valid
