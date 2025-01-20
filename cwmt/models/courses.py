from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    course_name = Column(String(100), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location_id = Column(Integer, db.ForeignKey('locations.id'), nullable=False)
    primary_instructor_id = Column(Integer, db.ForeignKey('instructors.id'), nullable=False)
    secondary_instructor_id = Column(Integer, db.ForeignKey('instructors.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    sessions = db.relationship('CourseSession', backref='course', lazy=True)
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
