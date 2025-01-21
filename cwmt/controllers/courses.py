from flask import Blueprint, flash, redirect, render_template, request, url_for
from cwmt.models.courses import Course
from cwmt import db

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
def index():
    all_courses = Course.get_all()
    context = {
        'all_courses': all_courses
    }
    return render_template('pages/courses/index.html', **context)

@courses_bp.route('/courses/<int:id>', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return render_template('courses/show.html', course=course)

@courses_bp.route('/courses', methods=['POST'])
def create_course():
    if request.method == 'POST':
        try:
            Course.create(request.form)
            return redirect(url_for('courses.index'))
        except Exception as e:
            print(f"Error (C-Course-001): creating course: {e}")
            flash(f"Error (C-Course-001): creating course: {e}", 'error')
            return redirect(url_for('courses.index'))
        
    return redirect(url_for('courses.index'))


@courses_bp.route('/courses', methods=['PUT'])
def update_course():
    

    return redirect(url_for('courses.index'))

@courses_bp.route('/courses/delete', methods=['POST'])
def delete_course():
    try:
        Course.delete_one(request.form.get('id'))
    except Exception as e:
        print(f"Error (C-Course-002): deleting course: {e}")
        flash(f"Error (C-Course-002): deleting course: {e}", 'error')
    return redirect(url_for('courses.index'))