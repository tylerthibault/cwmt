from flask import Blueprint, request, render_template, redirect, session, url_for, flash
from management.config import helper
from management.models import users, log

users_bp = Blueprint('users', __name__)

@users_bp.route('/users', methods=['GET'])
def get_users():
    return render_template('users.html', users=users)

@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if user:
        return render_template('user.html', user=user)
    flash('User not found', 'error')
    return redirect(url_for('users.get_users'))

@users_bp.route('/users/new', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        is_valid = users.User.validate_create(**request.form)
        if not is_valid:
            return redirect(url_for('routes.index'))
        
        user = users.User.create(**request.form)
        flash('User created successfully')

        log.Log.create(user, f"created and logged in")
        
        return redirect(url_for('users.get_users'))
    return 'error'
    # return render_template('create_user.html')

@users_bp.route('/users/login', methods=['POST'])
def login_user():
    user = users.User.validate_login(**request.form)

    if not user:
        return redirect(url_for('routes.index'))
    
    log.Log.create(user, 'logged in')

    return redirect(url_for('routes.dashboard'))

@users_bp.route('/users/logout', methods=['GET'])
def logout_user():
    user = helper.get_logged_in_user()
    log.Log.create(user, 'logged out')
    session.clear()
    return redirect(url_for('routes.index'))

@users_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def update_user(user_id):
    user = next((user for user in users if user['id'] == user_id), None)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('users.get_users'))
    
    if request.method == 'POST':
        user.update(request.form.to_dict())
        flash('User updated successfully', 'success')
        return redirect(url_for('users.get_user', user_id=user_id))
    
    return render_template('edit_user.html', user=user)

@users_bp.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    global users
    users = [user for user in users if user['id'] != user_id]
    flash('User deleted successfully', 'success')
    return redirect(url_for('users.get_users'))

@users_bp.route('/users/settings', methods=['GET'])
def settings():
    return render_template('settings.html')