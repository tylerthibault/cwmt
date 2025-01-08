from functools import wraps
from flask import session, redirect, url_for
from management.models import log
from datetime import datetime, timedelta

def require_user_hash(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_hash' not in session:
            return redirect(url_for('routes.index'))
        
        log = log.Log.query.filter_by(user_hash=session['user_hash']).first()
        if not log:
            return redirect(url_for('routes.index'))
        
        current_time = datetime.now()
        if (current_time - log.updated_at) > timedelta(minutes=10):
            return redirect(url_for('users.logout'))

        # If found, proceed with the original function
        return f(*args, **kwargs)
    return decorated_function