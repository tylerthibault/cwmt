from functools import wraps
from flask import redirect, url_for, session
from cwmt.models.logbook import LogBook
from cwmt import core


def login_required(func):
    """
    Custom decorator that checks session token validity before function execution.
    """
    @wraps(func)
    def login_required_wrapper(*args, **kwargs):
        # Pre-processing: check session token validity
        if not check_session_token():
            core.logger.log('Session token invalid or expired.', with_flash=True, status='error')
            return redirect(url_for('main.index'))  # Redirect to login if token is invalid

        log_entry = check_session_token()
        if not log_entry:
            core.logger.log('Session token invalid or expired.', with_flash=True, status='error')
            return redirect(url_for('login'))
        
        token = session.get('session_token')
        LogBook.update_timestamp(token)
        session['role'] = log_entry.user_role

        # Call the original function
        result = func(*args, **kwargs)

        # Post-processing logic
        return result
    return login_required_wrapper

def update_timestamp(func):
        """
        Custom decorator that wraps function execution in try/except block.
        """
        @wraps(func)
        def update_timestamp_handler(*args, **kwargs):
            try:
                is_valid = check_session_token()
                if is_valid:
                    LogBook.update_timestamp(session.get('session_token'))

                return func(*args, **kwargs)
            except Exception as e:
                core.logger.log(f'Error occurred: {str(e)}', with_flash=False, status='error')
                return redirect(url_for('error'))
        return update_timestamp_handler

def check_session_token():
    """
    Check the validity of the session token stored in the session.
    """
    session_token = session.get('session_token')
    if not session_token:
        return False
    
    # Check if session token exists in database and is not expired
    return LogBook.check_timestamp(session_token, max_age=600)
