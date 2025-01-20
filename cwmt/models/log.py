from flask import session
from cwmt import db, bcrypt
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    session_token = Column(String, nullable=False)
    user_id = Column(Integer, db.ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # FOREIGN KEYS
    # user = db.relationship('User', backref='logs', lazy=True)
    
    @classmethod
    def create(cls, user, action):
        statement = f'User {user.username} {datetime.datetime.now()}: {action}'
        log_data = {
            'user_id': user.id,
            'action': statement,
            'session_token': bcrypt.generate_password_hash(user.username + str(datetime.datetime.now())).decode('utf-8')
        }
        log = cls(**log_data)
        db.session.add(log)
        db.session.commit()

        session['session_token'] = log.session_token

        return log

    def update_record_timestamp(self):
        self.updated_at = datetime.datetime.now()
        db.session.commit()


