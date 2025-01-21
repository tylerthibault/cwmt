from flask import flash
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relationships
    # user = db.relationship('User', backref='roles', lazy=True)
    role = db.relationship('Role', backref='users', lazy=True)

    def __repr__(self):
        return self.role.name

    @classmethod
    def create(cls, data:dict):
        """
        Create a new user role record in the database

        args data: dict: A dictionary containing the user role's data
        dict: user_id, role_id

        returns UserRole: A UserRole object
        """
        try:
            data = {**data}
            user_role = cls(
                user_id=data['user_id'],
                role_id=data['role_id']
            )
            db.session.add(user_role)
            db.session.commit()
            return user_role
        except Exception as e:
            flash(f"Error (M-UserRoles-001) creating user role: {e}", 'error')
            print(f"Error (M-UserRoles-001) creating user role: {e}")
            return None


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    @classmethod
    def create(cls, data:dict):
        """
        Create a new role record in the database

        args data: dict: A dictionary containing the role's data
        dict: name, description

        returns Role: A Role object
        """
        try:
            data = {**data}
            role = cls(
                name=data['name'],
                description=data.get('description')
            )
            db.session.add(role)
            db.session.commit()
            return role
        except Exception as e:
            print(f"Error (M-Roles-001) creating role: {e}")
            flash(f"Error (M-Roles-001) creating role: {e}", 'error')
            return None

