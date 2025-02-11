from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import app

db = app.db
bcrypt = app.bcrypt

# -------------------------
# CohortTemplates Table
# -------------------------
class CohortTemplates(db.Model):
    __tablename__ = 'cohort_templates'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    default_max_capacity = db.Column(db.Integer, nullable=False)
    default_number_of_days = db.Column(db.Integer, nullable=False)
    default_location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)

    location = db.relationship('Locations', backref='cohort_templates')

    @classmethod
    def create(cls, data:dict):
        cohort_template = cls(
            name=data['name'],
            description=data.get('description', None),
            default_max_capacity=data.get('default_max_capacity', 10),
            default_number_of_days=data.get('default_number_of_days', 10),
            default_location_id=data['default_location_id']
        )
        db.session.add(cohort_template)
        db.session.commit()
        return cohort_template
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        cohort_template = cls.get_by_id(data['id'])
        for key, value in data.items():
            setattr(cohort_template, key, value)
        db.session.commit()
        return cohort_template
    
    
    @classmethod
    def delete(cls, id):
        cohort_template = cls.get_by_id(id)
        db.session.delete(cohort_template)
        db.session.commit()
        return cohort_template