from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.cohorts import Cohort
from cwmt.models.locations import Location
from cwmt.models.templates import Template
from cwmt.models.teams import Team

from cwmt.config.page_tracker import get_previous_page, track_page, get_current_page

from cwmt import core
import datetime  # added import

# Create a Blueprint instance
cohorts_bp = Blueprint('cohorts', __name__)

@cohorts_bp.route('/dashboard/cohorts')
@track_page
def dash_index():
    context = {
        'user': User.get(session.get('user')),
        'tab': request.args.get('tab', 'cohorts'),
        'locations': Location.get_all(),
        'cohorts': Cohort.get_all(),
        'templates': Template.get_all(),
        'teams': Team.get_all(),
        'now': datetime.datetime.utcnow() - datetime.timedelta(days=7)
    }
    return render_template('pages/private/dashboard/cohorts/base.html', **context)

@cohorts_bp.get('/dashboard/cohorts/archived')
@track_page
def archived():
    context = {
        'user': User.get(session.get('user')),
        'tab': request.args.get('tab', 'cohorts'),
        'locations': Location.get_all(),
        'cohorts': Cohort.get_all(),
        'templates': Template.get_all(),
        'teams': Team.get_all(),
        'now': datetime.datetime.utcnow() - datetime.timedelta(days=7)
    }
    return render_template('pages/private/dashboard/cohorts/archived.html', **context)

@cohorts_bp.post('/dashboard/cohorts/create')
def create():
    data = {**request.form}
    Cohort.create(data)
    return redirect(url_for('cohorts.dash_index', tab='cohorts'))

@cohorts_bp.route('/dashboard/cohorts/template/<int:template_id>', methods=['GET'])
def get_template_defaults(template_id):
    template = Template.get(template_id)
    if template:
        defaults = {
            "default_max_capacity": template.default_max_capacity,
            "default_number_of_days": template.default_number_of_days,
            "default_name": template.default_name
        }
        return jsonify(defaults)
    return jsonify({}), 404


@cohorts_bp.post('/api/dashboard/cohorts/update')
def update():
    try:
        id = request.form.get('id')
        cohort = Cohort.get(id)
        if not cohort:
            core.logger.log(f'Cohort with ID {id} not found.', with_flash=True, status='error')
            return jsonify({'status': 'error'})
        
        cohort.update(id, request.form)
        core.logger.log(f'Cohort {cohort.name} updated.', with_flash=True, flash_category='success')
        return jsonify({'status': 'success'})
    except Exception as e:
        core.logger.log(f'Error updating cohort: {e}', with_flash=True, status='error')
        return jsonify({'status': 'error'})

@cohorts_bp.get('/dashboard/cohorts/<int:id>/delete')
def delete(id):
    Cohort.delete(id)
    return redirect(url_for('cohorts.dash_index', tab='cohorts'))

@cohorts_bp.get('/dashboard/cohorts/<int:id>/assign_instructor')
@cohorts_bp.post('/dashboard/cohorts/<int:id>/assign_instructor')
def assign_instructor(id):
    role = request.args.get('role')
    cohort = Cohort.get(id)
    if request.method == 'POST':
        instructor_id = request.form.get('instructor_id')
        data = {}
        if role == 'primary':
            data['primary_instructor_id'] = instructor_id
        elif role == 'secondary':
            data['secondary_instructor_id'] = instructor_id

        data['id'] = id
        Cohort.update(data)
        core.logger.log(f'{role.capitalize()} instructor assigned for cohort {cohort.name}.', with_flash=True, flash_category='success')
        return redirect(get_current_page())
    return redirect(get_current_page())

@cohorts_bp.get('/dashboard/cohorts/<int:id>/unassign_instructor')
def unassign_instructor(id):
    role = request.args.get('role')
    cohort = Cohort.get(id)
    if not cohort:
        core.logger.log(f'Cohort with ID {id} not found.', with_flash=True, status='error')
        return redirect(get_current_page())
    
    data = {'id': id}
    if role == 'primary':
        data['primary_instructor_id'] = None
    elif role == 'secondary':
        data['secondary_instructor_id'] = None
    else:
        core.logger.log('Invalid role for instructor unassignment.', with_flash=True, status='error')
        return redirect(get_current_page())
    
    Cohort.update(data)
    core.logger.log(f'{role.capitalize()} instructor unassigned for cohort {cohort.name}.', with_flash=True, flash_category='success')
    return redirect(get_current_page())
