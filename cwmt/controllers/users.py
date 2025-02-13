from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from cwmt import core
from cwmt.models.users import User

# Create a Blueprint instance
users_bp = Blueprint('users', __name__)

@users_bp.post('/login')
def check_login():
    pass

# CREATE
@users_bp.post('/users/create')
def create():
    data = {**request.form}
    User.create(data)
    return redirect(url_for('teams.dash_index', tab='members'))
# READ

# UPDATE
@users_bp.post('/api/users/update')
def api_update():
    id = request.form.get('id')
    user = User.get(id)
    data = {**request.form}
    if not user:
        core.logger.log(f'User with ID {id} not found.', with_flash=True, status='error')
        return jsonify({'status': 'error'})
    
    User.update(id, data)
    return jsonify({'status': 'success'})

# DELETE
@users_bp.route('/users/<int:id>/delete')
def delete(id):
    User.delete(id)
    return redirect(url_for('teams.dash_index', tab='members'))