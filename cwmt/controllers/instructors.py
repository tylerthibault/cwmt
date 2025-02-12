from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/dashboard/instructors')
def dash_index():
    context = {
        'user': User.get(session.get('user'))
    }
    return render_template('pages/private/dashboard/instructors/index.html', **context)