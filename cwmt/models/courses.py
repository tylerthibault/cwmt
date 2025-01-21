from flask import flash
from cwmt import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @classmethod
    def create(cls, data: dict):
        """
        Create a new course record in the database

        args data: dict: A dictionary containing the course's data
        dict: course_name, primary_instructor_id, secondary_instructor_id

        returns Course: A Course object
        """
        data={**data}
        try:
            course = cls(
                name=data['name'],
                description=data.get('description'),
            )
            db.session.add(course)
            db.session.commit()
            flash(f"Course {course.name} created successfully", 'success')
            return course
        except Exception as e:
            print(f"Error (M-Course-001) creating course: {e}")
            flash(f"Error (M-Course-001) creating course: {e}", 'error')
            db.session.rollback()
            return None
        
    @classmethod
    def get_all(cls):
        """
        Get all courses

        returns list: A list of Course objects
        """
        return cls.query.all()

    @classmethod
    def delete_one(cls, id):
        """
        Delete a course

        args id: int: The id of the course to delete

        returns bool: True if successful, False otherwise
        """
        print(f"Deleting course with id {id}")
        try:
            course = cls.query.get(id)
            db.session.delete(course)
            db.session.commit()
            flash(f"Course {course.name} deleted successfully", 'success')
            return True
        except Exception as e:
            print(f"Error (M-Course-002) deleting course: {e}")
            flash(f"Error (M-Course-002) deleting course: {e}", 'error')
            db.session.rollback()
            return False