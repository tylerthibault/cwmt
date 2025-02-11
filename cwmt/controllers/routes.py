from flask import Blueprint, render_template, request, jsonify

# Create a Blueprint instance
main_bp = Blueprint('main', __name__)

# Define routes using the blueprint
@main_bp.route('/')
def index():
    return render_template('pages/public/landing/index.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

# Example of a route with methods
@main_bp.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        # Process the data
        return jsonify({'status': 'success'})
    return jsonify({'message': 'GET request received'})

@main_bp.route('/login')
def login():
    return render_template('pages/public/login/index.html')