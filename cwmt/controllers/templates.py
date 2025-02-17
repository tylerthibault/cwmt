from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.templates import Template
from cwmt import core

# Create a Blueprint instance
templates_bp = Blueprint('templates', __name__)

@templates_bp.post('/templates/create')
def create():
    data = request.form.to_dict()
    template = Template.create(data)
    return redirect(url_for('cohorts.dash_index', tab='templates'))

@templates_bp.post('/api/dashboard/templates/update')
def update():
    id = request.form.get('id')
    template = Template.get_by_id(id=id)
    if not template:
        core.logger.log(f'Template with ID {id} not found.', with_flash=True, status='error')
        return jsonify({'status': 'error'})
    
    template.update(request.form)
    core.logger.log(f'Template {template.name} updated.', with_flash=True, flash_category='success')
    return jsonify({'status': 'success'})

@templates_bp.route('/dashboard/templates/<int:id>/delete')
def delete(id):
    Template.delete(id)
    return redirect(url_for('cohorts.dash_index', tab='templates'))
