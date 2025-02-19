from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.logbook import LogBook
from cwmt.utils.logbook import login_required

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
    session_token = LogBook.create({
        'user_id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'ip_address': request.remote_addr,
        'user_role': user.roles[0].name,
        'user_agent': request.headers.get('User-Agent')
    })
    session['session_token'] = session_token
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name

    # redirect to dashboard
    return redirect(url_for('main.dashboard'))

@main_bp.route('/logout')
def logout():
    session.pop('session_token', None)
    session.pop('first_name', None)
    session.pop('last_name', None)
    return redirect(url_for('main.index'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    context = {
        'user': User.get(session.get('user'))
    }
    return render_template('pages/private/dashboard/index.html', **context)

@main_bp.route('/api/update_timestamp')
def update_timestamp():
    session_token = session.get('session_token')
    LogBook.update_timestamp(session_token)
    return jsonify({'status': 'success'})


@main_bp.route('/seed')
def seed():
    from instance.seed import seed_data
    seed_data()
    return 'Seed data inserted successfully'

