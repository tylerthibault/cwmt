from functools import wraps

def login_required(func):
    """
    Custom decorator that does something before and after the function call.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # --- Pre-processing logic ---
            # For example, check permissions or log function call
            print('Executing login_required on', func.__name__)

            # Call the original function
            result = func(*args, **kwargs)

            # --- Post-processing logic ---
            # For example, modify the result or perform cleanup
            return result
        return wrapper
    return decorator
