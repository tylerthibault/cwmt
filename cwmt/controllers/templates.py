from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
templates_bp = Blueprint('templates', __name__)

# Index route is in with the cohorts controller