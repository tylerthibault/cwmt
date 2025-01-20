from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Location(db.Model):
    __tablename__ = 'locations'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    zip_code = Column(String(10), nullable=True)
    capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    classes = db.relationship('Class', backref='location', lazy=True)
