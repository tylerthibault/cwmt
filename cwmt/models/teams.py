from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core

app = core.app
db = app.db
bcrypt = app.bcrypt

# Add join table for teams and users
team_members = db.Table('team_members',
    db.Model.metadata,
    db.Column('team_id', db.Integer, db.ForeignKey('teams.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# -------------------------
# Team Table
# -------------------------
class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)


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
    