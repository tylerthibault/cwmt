from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import app

db = app.db
bcrypt = app.bcrypt

# -------------------------
# Cohort Table
# -------------------------
class Cohort(db.Model):
    __tablename__ = 'cohort'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    number_of_days = db.Column(db.Integer, nullable=False)

    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    cohort_template_id = db.Column(db.Integer, db.ForeignKey('cohort_templates.id'), nullable=False)

    location = db.relationship('Locations', backref='cohorts')
    team = db.relationship('Teams', backref='cohorts')
    cohort_template = db.relationship('CohortTemplates', backref='cohorts')

    @classmethod
    def create(cls, data:dict):
        cohort = cls(
            name=data['name'],
            max_capacity=data.get('max_capacity', 10),
            description=data.get('description', None),
            start_date=data['start_date'],
            number_of_days=data.get('number_of_days', 1),
            location_id=data['location_id'],
            team_id=data['team_id'],
            cohort_template_id=data['cohort_template_id']
        )
        db.session.add(cohort)
        db.session.commit()
        return cohort

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        cohort = cls.get_by_id(data['id'])
        for key, value in data.items():
            setattr(cohort, key, value)
        db.session.commit()
        return cohort
    
    @classmethod
    def delete(cls, id):
        cohort = cls.get_by_id(id)
        db.session.delete(cohort)
        db.session.commit()
        return cohort



# -------------------------
# CohortHasUsers Table
# -------------------------
class CohortHasUsers(db.Model):
    __tablename__ = 'cohort_has_users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    cohort_id = db.Column(db.Integer, db.ForeignKey('cohort.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role = db.Column(db.String(255), nullable=False)
    has_paid = db.Column(db.Boolean, default=False)


    @classmethod
    def create(cls, data:dict):
        cohort_has_users = cls(
            cohort_id=data['cohort_id'],
            user_id=data['user_id'],
            role=data['role'],
            has_paid=data.get('has_paid', False)
        )
        db.session.add(cohort_has_users)
        db.session.commit()
        return cohort_has_users
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        cohort_has_users = cls.get_by_id(data['id'])
        for key, value in data.items():
            setattr(cohort_has_users, key, value)
        db.session.commit()
        return cohort_has_users
    
    @classmethod
    def delete(cls, id):
        cohort_has_users = cls.get_by_id(id)
        db.session.delete(cohort_has_users)
        db.session.commit()
        return cohort_has_users