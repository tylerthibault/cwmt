from functools import wraps
from flask import session, redirect, url_for, flash, current_app, request
from management.models import log
from datetime import datetime, timedelta

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_token' not in session:
            current_app.config['admin_logger'].warning('Unauthorized access attempt')
            return redirect(url_for('routes.index'))
        
        log_record = log.Log.query\
            .filter_by(session_token=session['session_token'])\
            .order_by(log.Log.updated_at.desc())\
            .first()

        if not log_record:
            current_app.config['admin_logger'].warning(f'Invalid session token: {session["session_token"]}')
            return redirect(url_for('routes.index'))
        
        current_time = datetime.now()
        if (current_time - log_record.updated_at) > timedelta(minutes=10):
            current_app.config['admin_logger'].info(f'Session expired for user {log_record.user.username}')
            flash('Session expired. Please login again.')
            return redirect(url_for('users.logout_user'))
        
        # Log user activity
        current_app.config['user_logger'].info(
            f'User {log_record.user.username} accessed {request.path}'
        )
        
        log_record.update_record_timestamp()
        return f(*args, **kwargs)
    return decorated_function