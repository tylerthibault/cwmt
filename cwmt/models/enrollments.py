from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = Column(Integer, db.ForeignKey('students.id'), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
