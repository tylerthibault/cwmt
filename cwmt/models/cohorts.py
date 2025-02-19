from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core
from cwmt.models.teams import team_has_cohorts
from cwmt.models import teams
from cwmt.models import users

from cwmt.models.crud_base import CRUDModel

app = core.app
db = app.db
bcrypt = app.bcrypt

# Add join table for cohorts and users
cohort_students = db.Table('cohort_students',
    db.Column('cohort_id', db.Integer, db.ForeignKey('cohorts.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

cohort_locations = db.Table('cohort_locations',
    db.Model.metadata,
    db.Column('location_id', db.Integer, db.ForeignKey('locations.id'), primary_key=True),
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'), primary_key=True)
)

cohort_instructors = db.Table('instructors',
    db.Model.metadata,
    db.Column('instructor_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('cohort_id', db.Integer, db.ForeignKey('cohorts.id'), primary_key=True)
)

# -------------------------
# Cohort Table
# -------------------------
class Cohort(db.Model, CRUDModel):
    __tablename__ = 'cohorts'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    max_capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False)
    number_of_days = db.Column(db.Integer, nullable=False)
    primary_instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    secondary_instructor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    # RELATIONSHIPS
    students = db.relationship('User', secondary=cohort_students, backref='cohorts')
    teams = db.relationship(
        'Team',
        secondary=team_has_cohorts,
        back_populates='cohorts'
    )
    @property
    def team(self):
        return self.teams[0] if self.teams else None

    @property
    def primary_instructor(self):
        return users.User.get(self.primary_instructor_id)
    
    @property
    def secondary_instructor(self):
        return users.User.get(self.secondary_instructor_id)

    @classmethod
    def create(cls, data:dict):
        cohort = cls(
            name=data['name'],
            max_capacity=data.get('max_capacity', 10),
            description=data.get('description', None),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            number_of_days=data.get('number_of_days', 1),
        )
        db.session.add(cohort)
        team = teams.Team.get(data['team_id'])
        team.cohorts.append(cohort)
        db.session.commit()
        return cohort

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        cohort = cls.get(data['id'])
        for key, value in data.items():
            setattr(cohort, key, value)
        db.session.commit()
        return cohort
    
    @classmethod
    def delete(cls, id):
        cohort = cls.get(id)
        db.session.delete(cohort)
        db.session.commit()
        return cohort



# # -------------------------
# # CohortHasUsers Table
# # -------------------------
# class CohortHasUsers(db.Model):
#     __tablename__ = 'cohort_has_users'

#     id = db.Column(db.Integer, primary_key=True)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

#     cohort_id = db.Column(db.Integer, db.ForeignKey('cohorts.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     role = db.Column(db.String(255), nullable=False)
#     has_paid = db.Column(db.Boolean, default=False)


#     @classmethod
#     def create(cls, data:dict):
#         cohort_has_users = cls(
#             cohort_id=data['cohort_id'],
#             user_id=data['user_id'],
#             role=data['role'],
#             has_paid=data.get('has_paid', False)
#         )
#         db.session.add(cohort_has_users)
#         db.session.commit()
#         return cohort_has_users
    
#     @classmethod
#     def get_all(cls):
#         return cls.query.all()
    
#     @classmethod
#     def get(cls, id):
#         return cls.query.get(id)
    
#     @classmethod
#     def update(cls, data:dict):
#         cohort_has_users = cls.get(data['id'])
#         for key, value in data.items():
#             setattr(cohort_has_users, key, value)
#         db.session.commit()
#         return cohort_has_users
    
#     @classmethod
#     def delete(cls, id):
#         cohort_has_users = cls.get(id)
#         db.session.delete(cohort_has_users)
#         db.session.commit()
#         return cohort_has_users