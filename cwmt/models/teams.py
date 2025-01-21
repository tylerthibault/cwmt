from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Team(db.Model):
    __tablename__ = 'teams'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    owner_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)  # The admin who owns the team
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    instructors = db.relationship('Instructor', backref='team', lazy=True)


    @classmethod
    def create(cls, data:dict):
        """
        Create a new team record in the database

        args data: dict: A dictionary containing the team's data
        dict: name, owner_id

        returns Team: A Team object
        """
        try:
            data = {**data}
            team = cls(
                name=data['name'],
                owner_id=data['owner_id']
            )
            db.session.add(team)
            db.session.commit()
            return team
        except Exception as e:
            print(f"Error creating team: {e}")
            flash(f"Error creating team: {e}", 'error')
            return None
        
    @classmethod
    def get_all(cls, owner_id:int):
        """
        Get all teams for a given owner

        args owner_id: int: The id of the owner

        returns list: A list of Team objects
        """
        return cls.query.filter_by(owner_id=owner_id).all()