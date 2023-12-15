# routes/ping.py

from flask import Blueprint, jsonify

# Blueprint setup for 'ping' route
ping_blueprint = Blueprint('ping', __name__)

# Define route '/ping/' with method 'GET'
@ping_blueprint.route('/ping/', methods=['GET'])
def ping():
    """
    Health check endpoint returning application status.
    Includes application name, status, and version.
    """
    # Response with app details
    response = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    return jsonify(response)  # Return JSON response
