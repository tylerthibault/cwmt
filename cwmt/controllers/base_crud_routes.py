from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.cohorts import Cohort
from cwmt.models.locations import Location
from cwmt.models.templates import Template
from cwmt.models.teams import Team
from cwmt.models.roles import Role

from cwmt import core

# Create a Blueprint instance
base_routes_db = Blueprint('base_routes', __name__)

MODELS = {
            'cohort': Cohort,
            'user': User,
            'location': Location,
            'template': Template,
            'team': Team,
            'role': Role
        }

# @base_routes_db.post('/api/dashboard/<string:model_name>/create')
# def create(model_name):
#     try:
#         ModelClass = MODELS.get(model_name)
#         if not ModelClass:
#             core.logger.log(f'Invalid model name: {model_name}', with_flash=True, status='error')
#             return jsonify({'status': 'error'})

#         data = {**request.form}
#         ModelClass.create(data)
#         return jsonify({'status': 'success'})
#     except Exception as e:
#         core.logger.log(f'Error creating {model_name}: {e}', with_flash=True, status='error')
#         return jsonify({'status': 'error'})

@base_routes_db.post('/api/dashboard/<string:model_name>/update')
def update(model_name):
    try:
        id = request.form.get('id')
        ModelClass = MODELS.get(model_name)
        if not ModelClass:
            core.logger.log(f'Invalid model name: {model_name}', with_flash=True, status='error')
            return jsonify({'status': 'error'})

        instance = ModelClass.get(id)
        if not instance:
            core.logger.log(f'{model_name.title()} with ID {id} not found.', with_flash=True, status='error')
            return jsonify({'status': 'error'})
        
        instance.update(id, request.form)
        return jsonify({'status': 'success'})
    except Exception as e:
        core.logger.log(f'Error updating {model_name}: {e}', with_flash=True, status='error')
        return jsonify({'status': 'error'})