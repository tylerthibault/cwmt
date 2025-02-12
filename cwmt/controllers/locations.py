from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from cwmt.models.users import User

# Create a Blueprint instance
locations_bp = Blueprint('locations', __name__)

# Index route is in with the cohorts controller