from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from cwmt import core

app = core.app
db = app.db
bcrypt = app.bcrypt

# -------------------------
# Locations Table
# -------------------------
class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    street = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state = db.Column(db.String(255), nullable=True)
    zip_code = db.Column(db.String(255), nullable=True)

    # RELATIONSHIPS

    @classmethod
    def create(cls, data:dict):
        location = cls(
            name=data['name'],
            description=data.get('description', None),
            street=data.get('street', None),
            city=data.get('city', None),
            state=data.get('state', None),
            zip_code=data.get('zip_code', None)
        )
        db.session.add(location)
        db.session.commit()
        core.logger.log(f'Location {location.name} created.', with_flash=True, flash_category='success')
        return location
    
    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def update(cls, data:dict):
        location = cls.get_by_id(data['id'])
        for key, value in data.items():
            setattr(location, key, value)
        db.session.commit()
        return location
    
    
    @classmethod
    def delete(cls, id):
        location = cls.get_by_id(id)
        db.session.delete(location)
        db.session.commit()
        return location
    