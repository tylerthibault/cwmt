from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt import core
from cwmt.models.users import User
from cwmt.models.locations import Location

# Create a Blueprint instance
locations_bp = Blueprint('locations', __name__)

@locations_bp.post('/create')
def create():
    data = request.form.to_dict()
    location = Location.create(data)
    return redirect(url_for('cohorts.dash_index', tab='locations'))

@locations_bp.route('/delete/<int:id>')
def delete(id):
    Location.delete(id)
    return redirect(url_for('cohorts.dash_index', tab='locations'))


@locations_bp.post('/api/dashboard/locations/update')
def update():
    id = request.form.get('id')
    location = Location.get_by_id(id=id)
    if not location:
        core.logger.log(f'Location with ID {id} not found.', with_flash=True, status='error')
        return jsonify({'status': 'error'})
    
    location.update(request.form)
    core.logger.log(f'Location {location.name} updated.', with_flash=True, flash_category='success')
    return jsonify({'status': 'success'})
