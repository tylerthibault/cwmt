from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

from management.config.decorators import login_required

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('/pages/index.html')

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    flash('You are logged in', 'success')
    flash('You are logged in', 'error')
    flash('You are logged in')
    return render_template('/pages/dashboard.html')

@routes_bp.route('/examples')
def examples():
    return render_template('/pages/examples/main.html')

@routes_bp.route('/examples/<string:page>')
def examples_page(page):
    return render_template(f'/pages/examples/{page}.html')
