from flask import Blueprint, render_template, request, jsonify

# Create a Blueprint instance
main = Blueprint('main', __name__)

# Define routes using the blueprint
@main.route('/')
def index():
    return render_template('pages/public/landing/index.html')

@main.route('/about')
def about():
    return render_template('about.html')

# Example of a route with methods
@main.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data = request.json
        # Process the data
        return jsonify({'status': 'success'})
    return jsonify({'message': 'GET request received'})