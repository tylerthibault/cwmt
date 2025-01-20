from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    pin = Column(String(4), nullable=True)
    user_level = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # FOREIGN KEYS
    logs = db.relationship('Log', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def create(cls, **kwargs):
        table_columns = [column.name for column in cls.__table__.columns]
        user_data = {key: value for key, value in kwargs.items() if key in table_columns}
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = cls(**user_data)
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def validate_login(**kwargs):
        is_valid = True

        for key, value in kwargs.items():
            if not value:
                is_valid = False

        if not is_valid:
            flash('All fields are required', 'error')

        user = User.query.filter_by(username=kwargs['username']).first()
        if not user:
            user = User.query.filter_by(email=kwargs['username']).first()

        if not user:
            print('User not found!!')
            flash('Invalid login creditials', 'error')
            is_valid = False
        
        if user and not bcrypt.check_password_hash(user.password, kwargs['password']):
            flash('Invalid login creditials', 'error')
            is_valid = False
        
        return user
        
    @staticmethod
    def validate_create(**kwargs):
        is_valid = True

        for key, value in kwargs.items():
            if not value:
                is_valid = False
            
        if not is_valid:
            flash('All fields are required', 'error')

        user = User.query.filter_by(username=kwargs['username']).first()

        if user:
            flash('Username already exists', 'error')
            is_valid = False

        return is_valid
    