from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import app

db = app.db
bcrypt = app.bcrypt

# Add join table for teams and users
team_members = db.Table('team_members',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# -------------------------
# Team Table
# -------------------------
class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)

    # Updated relationship to use the join table object
    members = db.relationship('User', secondary=team_members, back_populates='teams', lazy='dynamic')

    @classmethod
    def create(cls, name):
        team = cls(name=name)
        db.session.add(team)
        db.session.commit()
        return team
    
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
        team = cls.query.get(data['id'])
        for key, value in data.items():
            setattr(team, key, value)
        db.session.commit()
        return team
    
    @classmethod
    def delete(cls, id):
        team = cls.query.get(id)
        db.session.delete(team)
        db.session.commit()
        return
    

# -------------------------
# TeamHasUsers Table
# -------------------------
class TeamHasUsers(db.Model):
    __tablename__ = 'team_has_users'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    @classmethod
    def create(cls, team_id, user_id):
        team_has_users = cls(team_id=team_id, user_id=user_id)
        db.session.add(team_has_users)
        db.session.commit()
        return team_has_users
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def get_by_team_id(cls, team_id):
        return cls.query.filter_by(team_id=team_id).all()
    
    @classmethod
    def get_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def update(cls, data:dict):
        team_has_users = cls.query.get(data['id'])
        for key, value in data.items():
            setattr(team_has_users, key, value)
        db.session.commit()
        return team_has_users
    
    @classmethod
    def delete(cls, id):
        team_has_users = cls.query.get(id)
        db.session.delete(team_has_users)
        db.session.commit()
        return
