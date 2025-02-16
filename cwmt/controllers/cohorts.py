from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.cohorts import Cohort
from cwmt.models.locations import Location
from cwmt.models.templates import Template
from cwmt.models.teams import Team

# Create a Blueprint instance
cohorts_bp = Blueprint('cohorts', __name__)

@cohorts_bp.route('/dashboard/cohorts')
def dash_index():
    context = {
        'user': User.get(session.get('user')),
        'tab': request.args.get('tab', 'cohorts'),
        'locations': Location.get_all(),
        'cohorts': Cohort.get_all(),
        'templates': Template.get_all(),
        'teams': Team.get_all()
    }
    return render_template('pages/private/dashboard/cohorts/base.html', **context)

@cohorts_bp.post('/dashboard/cohorts/create')
def create():
    data = {**request.form}
    Cohort.create(data)
    return redirect(url_for('cohorts.dash_index', tab='cohorts'))

@cohorts_bp.route('/dashboard/cohorts/template/<int:template_id>', methods=['GET'])
def get_template_defaults(template_id):
    template = Template.get_by_id(template_id)
    if template:
        defaults = {
            "default_max_capacity": template.default_max_capacity,
            "default_number_of_days": template.default_number_of_days
        }
        return jsonify(defaults)
    return jsonify({}), 404