from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/dashboard/teams')
def dash_index():
    context = {
        'user': User.get(session.get('user'))
    }
    return render_template('pages/private/dashboard/teams/index.html', **context)