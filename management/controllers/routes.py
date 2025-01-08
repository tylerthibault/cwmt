from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash

from management.config.decorators import login_required

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    return render_template('/pages/index.html')

@routes_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('/pages/dashboard.html')
