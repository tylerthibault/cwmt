from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.cohorts import Cohort
from cwmt.models.locations import Location
from cwmt.models.templates import Template
from cwmt.models.teams import Team
from cwmt.models.roles import Role

from cwmt import core

# Create a Blueprint instance
main_bp = Blueprint('main', __name__)

# Define routes using the blueprint
@main_bp.route('/')
def index():
    return render_template('pages/public/landing/index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/login')
def login():
    return render_template('pages/public/login/index.html')

@main_bp.post('/login')
def check_login():
    # validate
    data = {**request.form}
    user = User.validate_login(data)

    if not user:
        return redirect(url_for('main.login'))

    # create session
    session['user'] = user.id

    # redirect to dashboard
    return redirect(url_for('main.dashboard'))

@main_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
def dashboard():
    context = {
        'user': User.get(session.get('user'))
    }
    return render_template('pages/private/dashboard/index.html', **context)


@main_bp.route('/seed')
def seed():
    from instance.seed import seed_data
    seed_data()
    return 'Seed data inserted successfully'

