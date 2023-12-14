# routes/ping.py

from flask import Blueprint, jsonify

# Create a Blueprint for the ping route
ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping/', methods=['GET'])
def ping():
    """
    Health check endpoint. Returns basic information about the application,
    including its name and version.
    """
    response = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    return jsonify(response)
