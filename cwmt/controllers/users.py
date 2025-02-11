from flask import Blueprint, render_template, request, jsonify
from cwmt.models.users import User

# Create a Blueprint instance
users_bp = Blueprint('users', __name__)

@users_bp.post('/login')
def check_login():
    pass

# CREATE
@users_bp.post('/api/users/create')
def api_create_user():
    user = User.create(request.form)
    if user:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'fail'})

@users_bp.post('/users/create')
def create_user():
    user = User.create(request.form)
    if user:
        return 'User created successfully'
    return 'User creation failed'
# READ

# UPDATE

# DELETE