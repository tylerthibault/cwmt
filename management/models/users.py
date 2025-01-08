from flask import flash
from management import db
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

    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def create(cls, **kwargs):
        pass

    @staticmethod
    def validate(**kwargs):
        is_valid = True

        for key, value in kwargs.items():
            if not value:
                is_valid = False
            
        flash('All fields are required', 'error')

        return is_valid