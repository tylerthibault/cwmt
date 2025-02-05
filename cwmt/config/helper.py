from flask import session
from cwmt.models import users, log, instructors


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
        session['user']['roles'] = user.roles[0].role.name if user.roles else None
        if session['user']['roles'] == 'instructor':
            instructor_info = instructors.Instructor.query.filter_by(user_id=user.id).first()
            session['user']['team_id'] = instructor_info.team_id
            session['user']['instructor_id'] = instructor_info.id
        return user
    return None

def get_user_id():
    user = get_logged_in_user()
    return user.id if user else None

def clear_session_user_data():
    user = get_logged_in_user()
    session.pop('user', None)
    session.pop('session_token', None)
    return user
