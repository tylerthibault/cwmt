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
    def create(cls, data: dict):
        is_valid = cls.validate(data)
        if not is_valid:
            return None

        team = cls(name=data.get('name'))
        db.session.add(team)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            core.logger.log(f'Error creating team: {e}', with_flash=True, status='error')
            return None

        core.logger.log(f'Team {team.name} created.', with_flash=True, flash_category='success')
        return team
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        print(id)
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
    
    @staticmethod
    def validate(data:dict):
        is_valid = True

        if not data.get('name'):
            is_valid = False
            core.logger.log('name is required.', with_flash=True, status='error')
        elif Team.get_by_name(data.get('name')):
            is_valid = False
            core.logger.log('Name must be unique.', with_flash=True, status='error')
   
        
        return is_valid
    