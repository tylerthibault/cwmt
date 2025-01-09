from flask import flash
from management import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Settings(db.Model):
    __tablename__ = 'settings'
    id = Column(Integer, primary_key=True)
    site_name = Column(String(100), nullable=False, default='My Site')
    site_description = Column(String(500), nullable=True)
    maintenance_mode = Column(Integer, default=0)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)