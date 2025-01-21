from flask import flash
from cwmt import db, bcrypt
from cwmt.config.helper import get_logged_in_user
from cwmt.models.users import User
from cwmt.models.roles import Role, UserRole
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
import datetime

class Instructor(db.Model):
    __tablename__ = 'instructors'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)  # Links to the User table
    team_id = Column(Integer, db.ForeignKey('teams.id'), nullable=False)  # Links to the Team table
    bio = Column(String(255), nullable=True)  # Optional additional details about the instructor
    certifications = Column(String(255), nullable=True)  # Optional list of certifications
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref='instructor_profile', uselist=False, lazy=True)

    @classmethod
    def create_new_instructor(cls, data:dict):
        """
        Create a new instructor record in the database

        args data: dict: A dictionary containing the instructor's data
        dict: user_id, team_id, bio, certifications

        returns Instructor: An Instructor object
        """
        print("*"*80)
        # create a User object
        data = {**data}
        data['username'] = f"{data['first_name']} {data['last_name']}"
        data['password'] = f"{data['first_name']}.{data['last_name']}.{data['phone_number'][-4:]}"
        user = User.create(data)
        print("*"*80)
        # get the team_id
        team_id = data['team_id']

        # create an Instructor object
        data['user_id'] = user.id
        instructor = cls.create(data)
        print("*"*80)
        # find the id for "instructor" role
        role_id = Role.query.filter_by(name="instructor").first().id

        print(f"Role ID: {role_id}")
        print("*"*80)
        # add user to UserRole table
        UserRole.create({'user_id': user.id, 'role_id': role_id})

        return instructor

    @classmethod
    def create(cls, data:dict):
        """
        Create a new instructor record in the database

        args data: dict: A dictionary containing the instructor's data
        dict: user_id, team_id, bio, certifications

        returns Instructor: An Instructor object
        """
        try:
            data = {**data}
            instructor = cls(
                user_id=data['user_id'],
                team_id=data['team_id'],
                # bio=data.get('bio'),
                # certifications=data.get('certifications')
            )
            db.session.add(instructor)
            db.session.commit()
            return instructor
        except Exception as e:
            print(f"Error creating instructor: {e}")
            flash(f"Error creating instructor: {e}", 'error')
            return None
