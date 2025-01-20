from flask import flash
from cwmt import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class CourseSession(db.Model):
    __tablename__ = 'course_sessions'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, db.ForeignKey('courses.id'), nullable=False)
    session_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    instructor_id = Column(Integer, db.ForeignKey('instructors.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
