from flask import Blueprint, flash, redirect, render_template, request, url_for
from cwmt.models.courses import Course, CourseSession
from cwmt.config.app_core import AppCore
from datetime import datetime

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/courses', methods=['GET'])
def index():
    tab = request.args.get('tab', 'course-calendar')
    print(f"Tab: {tab}")
    context = {
        'active_tab': tab,
        'all_courses': Course.get_all(),
        'all_course_sessions_a': CourseSession.get_all(),
        'all_course_sessions': [session.to_dict() for session in CourseSession.query.all()],
        
    }
    return render_template('pages/courses/index.html', **context)

# @courses_bp.route('/courses/<int:id>', methods=['GET'])
# def get_course(id):
#     course = Course.query.get_or_404(id)
#     return render_template('courses/show.html', course=course)

@courses_bp.route('/courses/create', methods=['POST'])
def create():
    if request.method == 'POST':
        try:
            Course.create(request.form)
        except Exception as e:
            AppCore.MyLogger.log(e, AppCore.StatusCodes.e_creating_course, should_print=True, should_flash=True)
        
    return redirect(url_for('courses.index', tab="courses"))


@courses_bp.route('/courses/update', methods=['POST'])
def update():
    try:
        Course.update_one(request.form)
    except Exception as e:
        AppCore.MyLogger.log(e, AppCore.StatusCodes.e_updating_course, should_print=True, should_flash=True)

    return redirect(url_for('courses.index', tab="courses"))

@courses_bp.route('/courses/delete', methods=['POST'])
def delete():
    try:
        Course.delete_one(request.form.get('id'))
    except Exception as e:
        AppCore.MyLogger.log(e, AppCore.StatusCodes.e_deleting_course, should_print=True, should_flash=True)
    return redirect(url_for('courses.index', tab="courses"))


# Course Sessions

course_sessions_bp = Blueprint('course_sessions', __name__)

@course_sessions_bp.route('/course_sessions/create', methods=['POST'])
def create():
    try:
        CourseSession.create(request.form)
    except Exception as e:
        AppCore.MyLogger.log(e, AppCore.StatusCodes.e_creating_course_session, should_print=True, should_flash=True)
    return redirect(url_for('courses.index', tab="course-sessions"))