from management import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime

class Log(db.Model):
    __tablename__ = 'logs'
    
    id = Column(Integer, primary_key=True)
    user_hash = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    action = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    def __init__(self, user_id, action, page=None):
        self.user_id = user_id
        self.action = action
        self.page = page

