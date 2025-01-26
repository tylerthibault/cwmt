from flask import flash
from cwmt import db
from sqlalchemy import Column, Integer, String, DateTime
# import datetime
from datetime import datetime
from cwmt.config.app_core import AppCore
from cwmt.models.instructors import Instructor



class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    max_students = db.Column(db.Integer, nullable=True)
    total_days = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
                max_students=data.get('max_students'),
                total_days=data.get('total_days')
            )
            db.session.add(course)
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_creating_course, should_print=True, should_flash=True)
            return course
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_creating_course, e, should_print=True, should_flash=True)

            db.session.rollback()
            return None
        
    @classmethod
    def get_all(cls):
        """
        Get all courses

        returns list: A list of Course objects
        """
        try:
            return cls.query.all()
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_getting_courses, e, should_print=True, should_flash=True)
            return []
    

    @classmethod
    def update_one(cls, data:dict):
        """
        Update a course

        args data: dict: A dictionary containing the course's data
        dict: id, name, description

        returns bool: True if successful, False otherwise
        """
        try:
            course = cls.query.get(data['id'])
            course.name = data['name']
            course.description = data.get('description')
            course.max_students = data.get('max_students')
            course.total_days = data.get('total_days')
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_updating_course, should_print=True, should_flash=True)
            return True
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_updating_course, e, should_print=True, should_flash=True)
            db.session.rollback()
            return
        

    @classmethod
    def delete_one(cls, id):
        """
        Delete a course

        args id: int: The id of the course to delete

        returns bool: True if successful, False otherwise
        """
        try:
            course = cls.query.get(id)
            db.session.delete(course)
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_deleting_course, should_print=True, should_flash=True)
            return True
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_deleting_course, e, should_print=True, should_flash=True)
            db.session.rollback()
            return False
        
class CourseSession(db.Model):
    __tablename__ = 'course_sessions'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    primary_instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    secondary_instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def course(self):
        return Course.query.get(self.course_id)
    
    @property
    def primary_instructor(self):
        return Instructor.query.get(self.primary_instructor_id)
    
    @property
    def secondary_instructor(self):
        return Instructor.query.get(self.secondary_instructor_id)
    
    def to_dict(self):
        return {
            'id': self.id,
            'course_id': self.course_id,
            'date': self.date.strftime('%Y-%m-%d'),
            'start_time': self.start_time.strftime('%H:%M'),
            'location': self.location,
            'notes': self.notes,
            'primary_instructor_id': self.primary_instructor_id,
            'secondary_instructor_id': self.secondary_instructor_id,
            'total_days': self.course.total_days,
            'course': {
                'id': self.course.id,
                'name': self.course.name
            }
        }

    @classmethod
    def create(cls, data:dict):
        """
        Create a new course session record in the database

        args data: dict: A dictionary containing the course session's data
        dict: course_id, session_date, start_time, end_time, primary_instructor_id, secondary_instructor_id

        returns CourseSession: A CourseSession object
        """
        try:
            data = {**data}

            course_session = cls(
                course_id=data['course_id'],
                date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
                start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
                location=data['location'],
                primary_instructor_id=data.get('primary_instructor_id'),
                secondary_instructor_id=data.get('secondary_instructor_id'),
                notes=data.get('notes'),
            )
            db.session.add(course_session)
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_creating_course_session, should_print=True, should_flash=True)
            return course_session
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_creating_course_session, e, should_print=True, should_flash=True)
            db.session.rollback()
            return None
        
    @classmethod
    def get_all(cls):
        """
        Get all course sessions

        returns list: A list of CourseSession objects
        """
        try:
            return cls.query.all()
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_getting_course_sessions, e, should_print=True, should_flash=True)
            return None
        
    @classmethod
    def update_one(cls, data:dict):
        """
        Update a course session

        args data: dict: A dictionary containing the course session's data
        dict: session_id, course_id, session_date, start_time, end_time, primary_instructor_id, secondary_instructor_id

        returns bool: True if successful, False otherwise
        """
        try:
            # Debug print incoming data
            print("Received data:", data)

            
            course_session = cls.query.get(data['id'])
            print("Found session:", course_session)
            
            if not course_session:
                print("No session found with id:", data['session_id'])
                return False
            
            # Print each field update
            for key, value in data.items():
                if hasattr(course_session, key):
                    print(f"Updating {key}: {value}")
                    
            if 'course_id' in data:
                print("Setting course_id:", data['course_id'])
                course_session.course_id = data['course_id']
            if 'date' in data:
                print("Setting date:", data['date'])
                course_session.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            if 'start_time' in data:
                print("Setting start_time:", data['start_time'])
                course_session.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            if 'location' in data:
                print("Setting location:", data['location'])
                course_session.location = data['location']
            if 'notes' in data:
                print("Setting notes:", data['notes'])
                course_session.notes = data['notes']
            if 'primary_instructor_id' in data:
                print("Setting primary_instructor_id:", data['primary_instructor_id'])
                course_session.primary_instructor_id = data['primary_instructor_id']
            if 'secondary_instructor_id' in data:
                print("Setting secondary_instructor_id:", data['secondary_instructor_id'])
                course_session.secondary_instructor_id = data['secondary_instructor_id']
            
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_updating_course_session, should_print=True, should_flash=True)
            return True
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_updating_course_session, e, should_print=True, should_flash=True)
            db.session.rollback()
            return False
        
    @classmethod
    def delete_one(cls, data:dict):
        """
        Delete a course session

        args data: dict: A dictionary containing the course session's data
        dict: session_id

        returns bool: True if successful, False otherwise
        """
        try:
            course_session = cls.query.get(data['session_id'])
            db.session.delete(course_session)
            db.session.commit()
            AppCore.MyLogger.log(AppCore.StatusCodes.s_deleting_course_session, should_print=True, should_flash=True)
            return True
        except Exception as e:
            AppCore.MyLogger.log(AppCore.StatusCodes.e_deleting_course_session, e, should_print=True, should_flash=True)
            db.session.rollback()
            return False
        
