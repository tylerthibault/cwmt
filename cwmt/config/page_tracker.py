from functools import wraps   # added import
from flask import session, request
from typing import List, Optional

def track_page(f):
    @wraps(f)  # added wraps decorator
    def track_page_wrapper(*args, **kwargs):
        add_page_to_tracker(request.path)
        return f(*args, **kwargs)
    return track_page_wrapper

def add_page_to_tracker(page_name: str) -> None:
    """
    Add a page to the session tracker
    
    Args:
        page_name (str): Name or URL of the page to track
    """
    if 'page_tracker' not in session:
        session['page_tracker'] = []
    
    # Add the new page to the tracker if it's not the current page
    if not session['page_tracker'] or session['page_tracker'][-1] != page_name:
        # session['page_tracker'].append(page_name)
        pages = session['page_tracker']
        pages.append(page_name)
        session['page_tracker'] = pages

def get_page_history() -> List[str]:
    """
    Get the list of tracked pages
    
    Returns:
        List[str]: List of tracked pages in order of visit
    """
    return session.get('page_tracker', [])

def clear_page_tracker() -> None:
    """
    Clear the page tracking history
    """
    if 'page_tracker' in session:
        session.pop('page_tracker')

def get_previous_page() -> Optional[str]:
    """
    Get the previously visited page
    
    Returns:
        Optional[str]: The previous page name or None if no history exists
    """
    history = get_page_history()
    return history[-2] if len(history) >= 2 else None

def get_current_page() -> Optional[str]:
    """
    Get the current page name
    
    Returns:
        Optional[str]: The current page name or None if no history exists
    """
    history = get_page_history()
    return history[-1] if history else None