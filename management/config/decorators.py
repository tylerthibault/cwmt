from functools import wraps
from flask import session, redirect, url_for, flash
from management.models import log
from datetime import datetime, timedelta

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_token' not in session:
            return redirect(url_for('routes.index'))
        
        log_record = log.Log.query.filter_by(session_token=session['session_token']).first().order_by(log.Log.updated_at.desc())
        if not log_record:
            return redirect(url_for('routes.index'))
        
        current_time = datetime.now()
        if (current_time - log_record.updated_at) > timedelta(minutes=10):
            flash('Session expired. Please login again.')
            return redirect(url_for('users.logout_user'))
        
        log_record.add_record()
        # If found, proceed with the original function
        return f(*args, **kwargs)
    return decorated_function