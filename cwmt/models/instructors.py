from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime


class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone_number = Column(String(15), nullable=True)
    certifications = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    primary_classes = db.relationship('Class', foreign_keys='Class.primary_instructor_id', backref='primary_instructor', lazy=True)
    secondary_classes = db.relationship('Class', foreign_keys='Class.secondary_instructor_id', backref='secondary_instructor', lazy=True)
    sessions = db.relationship('ClassSession', backref='instructor', lazy=True)
