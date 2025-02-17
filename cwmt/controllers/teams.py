from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User
from cwmt.models.teams import Team
from cwmt.models.roles import Role
from cwmt import core

from cwmt.config.page_tracker import get_previous_page, track_page

# Create a Blueprint instance
teams_bp = Blueprint('teams', __name__)

@teams_bp.route('/dashboard/teams')
@track_page
def dash_index():
    selected_team_id = request.args.get('team_id', 1)  # added line
    context = {
        'user': User.get(session.get('user')),
        'tab': request.args.get('tab', 'teams'),
        'teams': Team.get_all(),
        'roles': Role.get_all(),
        'users': User.get_all(),
        'selected_team_id': selected_team_id  # added line
    }
    return render_template('pages/private/dashboard/teams/base.html', **context)

# CREATE
@teams_bp.post('/dashboard/teams/create')
def create():
    team = Team.create(request.form)
    return redirect(url_for('teams.dash_index', tab='teams'))

# READ


# UPDATE
@teams_bp.post('/api/dashboard/teams/update')
def update():
    id = request.form.get('id')
    team = Team.get(id=id)
    if not team:
        core.logger.log(f'Team with ID {id} not found.', with_flash=True, status='error')
        return jsonify({'status': 'error'})
    
    team.update(request.form)
    core.logger.log(f'Team {team.name} updated.', with_flash=True, flash_category='success')
    return jsonify({'status': 'success'})

@teams_bp.post('/dashboard/teams/add_user')
def add_user():
    data = {**request.form}
    Team.add_member(data)
    return redirect(url_for('teams.dash_index', tab='teams', team_id=data['team_id']))

@teams_bp.post('/dashboard/teams/remove_user')
def remove_user():
    data = {**request.form}
    Team.remove_member(data)
    return redirect(url_for('teams.dash_index', tab='teams', team_id=data['team_id']))

# DELETE
@teams_bp.route('/dashboard/teams/<int:id>/delete')
def delete(id):
    team = Team.get(id)
    if not team:
        return redirect(url_for('teams.dash_index', tab='teams'))
    
    team.delete(id)
    return redirect(url_for('teams.dash_index', tab='teams'))