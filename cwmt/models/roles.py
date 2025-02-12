from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core

from cwmt.models.users import user_roles

app = core.app
db = app.db
bcrypt = app.bcrypt

# -------------------------
# Roles Table
# -------------------------
class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    
    # # RELATIONSHIPS
    # users = db.relationship('User', secondary=user_roles, lazy='subquery', backref=db.backref('roles', lazy=True))

    @classmethod
    def create(cls, name):
        role = cls(name=name)
        db.session.add(role)
        db.session.commit()
        return role
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def update(cls, data:dict):
        role = cls.query.get(data['id'])
        for key, value in data.items():
            setattr(role, key, value)
        db.session.commit()
        return role
    
    @classmethod
    def delete(cls, id):
        role = cls.query.get(id)
        db.session.delete(role)
        db.session.commit()
        return role
    