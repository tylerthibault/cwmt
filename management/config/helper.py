from flask import session
from management.models import users, log


def get_logged_in_user():
    session_token = session.get('session_token')
    if not session_token:
        return None
    return users.User.query\
        .select_from(users.User)\
        .join(log.Log, users.User.id == log.Log.user_id)\
        .filter(log.Log.session_token == session_token)\
        .first()

def load_session_user_data():
    user = get_logged_in_user()
    if user:
        if 'user' not in session:
            session['user'] = {}
        session['user']['username'] = user.username
        session['user']['email'] = user.email
        return user
    return None

def clear_session_user_data():
    user = get_logged_in_user()
    session.pop('user', None)
    session.pop('session_token', None)
    return user