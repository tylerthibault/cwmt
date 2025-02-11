from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import app

db = app.db
bcrypt = app.bcrypt

# -------------------------
# Roles Table
# -------------------------
class Roles(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)

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
    
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    @classmethod
    def create(cls, user_id, role_id):
        user_role = cls(user_id=user_id, role_id=role_id)
        db.session.add(user_role)
        db.session.commit()
        return user_role
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_by_role_id(cls, role_id):
        return cls.query.filter_by(role_id=role_id).all()
    
    @classmethod
    def update(cls, data:dict):
        user_role = cls.query.get(data['id'])
        for key, value in data.items():
            setattr(user_role, key, value)
        db.session.commit()
        return user_role
    
    @classmethod
    def delete(cls, id):
        user_role = cls.query.get(id)
        db.session.delete(user_role)
        db.session.commit()
        return user_role