from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session
from cwmt.config.helper import load_session_user_data
from cwmt.config.seed import seed_db
from cwmt.config.decorators import login_required
# from cwmt.config.status_codes import ErrorCodes
from cwmt.config.app_core import AppCore
from cwmt.models.instructors import Instructor
from cwmt.models.courses import Course, CourseSession

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    
    return render_template('/pages/public/landing.html')

@routes_bp.route('/<string:page>')
def public_page(page):
    context = {
        'all_course_sessions': [session.to_dict() for session in CourseSession.query.all()],
    }
    return render_template(f'/pages/public/{page}.html', **context)

@routes_bp.route('/signup')
def calendar():
    context = {
        'all_course_sessions': [session.to_dict() for session in CourseSession.query.all()],
    }
    return render_template('/pages/public/signup.html', **context)

# TEST Routes

@routes_bp.route('/test/<string:page>')
def test_page(page):
    context = {
        'all_course_sessions': [session.to_dict() for session in CourseSession.query.all()],
    }
    return render_template(f'/pages/test/{page}.html', **context)

# Dashboards **************************

@routes_bp.route('/dashboard')
# @login_required
def dashboard():
    role = session['user']['roles']

    if role == 'sys-admin':
        return redirect(url_for('routes.sys_admin_dashboard'))
    elif role == 'admin':
        return redirect(url_for('routes.admin_dashboard'))
    elif role == 'instructor':
        return redirect(url_for('routes.instructor_dashboard'))
    elif role == 'student':
        return redirect(url_for('routes.student_dashboard'))
    else:
        return redirect(url_for('routes.index'))
    return render_template('/pages/admin//dashboard.html')

@routes_bp.route('/sys-admin/dashboard')
# @login_required
def sys_admin_dashboard():
    return render_template('/pages/admin//dashboard.html')

@routes_bp.route('/admin/dashboard')
# @login_required
def admin_dashboard():
    return render_template('/pages/admin//dashboard.html')

@routes_bp.route('/instructor/dashboard')
# @login_required
def instructor_dashboard():
    context = {
        'team': Instructor.get_team(session['user']['team_id'])
    }
    return render_template('/pages/instructors/dashboard.html', **context)

@routes_bp.route('/student/dashboard')
# @login_required
def student_dashboard():
    return render_template('/pages/student/dashboard.html')


@routes_bp.route('/examples')
# @login_required
def examples():
    return render_template('/pages/examples/main.html')

@routes_bp.route('/examples/<string:page>')
# @login_required
def examples_page(page):
    return render_template(f'/pages/examples/{page}.html')

@routes_bp.route('/seed')
def seed():
    seed_db()
    return redirect(url_for('routes.index'))