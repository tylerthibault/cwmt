from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from cwmt.config.seed import seed_db
from cwmt.config.decorators import login_required
# from cwmt.config.status_codes import ErrorCodes
from cwmt.config.app_core import AppCore

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('/pages/landing.html')

@routes_bp.route('/test/<int:num>')
def test(num):
    return render_template(f'/pages/test_pages/test{num}.html')   

@routes_bp.route('/dashboard')
# @login_required
def dashboard():
    return render_template('/pages/dashboard.html')

@routes_bp.route('/examples')
@login_required
def examples():
    return render_template('/pages/examples/main.html')

@routes_bp.route('/examples/<string:page>')
@login_required
def examples_page(page):
    return render_template(f'/pages/examples/{page}.html')

@routes_bp.route('/seed')
def seed():
    seed_db()
    return redirect(url_for('routes.index'))