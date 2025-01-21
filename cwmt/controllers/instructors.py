from flask import Blueprint, render_template, request, redirect, url_for, flash
from cwmt.config.helper import get_logged_in_user
from cwmt.models.instructors import Instructor
from cwmt.models.teams import Team
from cwmt import db

# Create blueprint
instructors_bp = Blueprint('instructors', __name__)

@instructors_bp.route('/instructors')
def index():
    teams = Team.get_all(get_logged_in_user().id)
    context = {
        'all_teams': teams,
    }
    return render_template('pages/instructors/index.html', **context)

@instructors_bp.route('/instructors/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            Instructor.create_new_instructor(request.form)
            return redirect(url_for('instructors.index'))
        except Exception as e:
            flash(f'Error creating instructor: {str(e)}', 'error')
            return redirect(url_for('instructors.index'))
        
    return redirect(url_for('instructors.index'))

@instructors_bp.route('/instructors/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    instructor = Instructor.query.get_or_404(id)
    if request.method == 'POST':
        instructor.name = request.form['name']
        instructor.email = request.form['email']
        instructor.phone = request.form['phone']
        db.session.commit()
        flash('Instructor updated successfully')
        return redirect(url_for('instructors.index'))
    return render_template('instructors/edit.html', instructor=instructor)

@instructors_bp.route('/instructors/<int:id>/delete', methods=['POST'])
def delete(id):
    instructor = Instructor.query.get_or_404(id)
    db.session.delete(instructor)
    db.session.commit()
    flash('Instructor deleted successfully')
    return redirect(url_for('instructors.index'))