from flask import session
from management.models import users, log


def get_logged_in_user():
    session_token = session.get('user_hash')
    return users.User.query.join(log.Log).filter(log.Log.session_token == session_token).first()