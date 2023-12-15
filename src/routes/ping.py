# routes/ping.py

from flask import Blueprint, jsonify

# Blueprint setup for the 'ping' route. This establishes a group of routes under the '/ping' URL.
ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping/', methods=['GET'])
def ping():
    """
    Health check endpoint that returns the application's status.

    This endpoint is useful for monitoring and verifying that the application is running.
    It returns basic information about the application, including its name, status, and version.

    Returns:
        Response: JSON response containing the application name, status, and version.
    """
    # Construct the response with application details.
    response = {
        "name": "weatherservice",
        "status": "ok",
        "version": "1.0.0"
    }
    # Return the response in JSON format.
    return jsonify(response)
