from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
cohorts_bp = Blueprint('cohorts', __name__)

@cohorts_bp.route('/dashboard/cohorts')
def dash_index():
    context = {
        'user': User.get(session.get('user')),
        'tab': request.args.get('tab', 'cohorts')
    }
    return render_template('pages/private/dashboard/cohorts/base.html', **context)