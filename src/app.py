from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from services.weather_service import WeatherService
from routes.ping import ping_blueprint
from routes.forecast import forecast_blueprint
import os
import yaml

# Define the root directory of the application.
WEATHER_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize HTTP Basic Authentication
auth = HTTPBasicAuth()

# Load user credentials from a YAML file
def load_user_credentials():
    users_config_path = os.path.join(WEATHER_ROOT_DIR, 'config', 'users.yaml')
    with open(users_config_path, 'r') as users_file:
        return yaml.safe_load(users_file)

USERS = load_user_credentials()

@auth.verify_password
def verify_password(username, password):
    if username in USERS and USERS[username] == password:
        return username

def create_app(testing=False):
    # Initialize the Flask application
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration
    config_filename = 'test-config.yaml' if testing else 'config.yaml'
    config_path = os.path.join(WEATHER_ROOT_DIR, 'config', config_filename)
    with open(config_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)
        app.config.update(config_data)

    # Initialize WeatherService
    weather_service = WeatherService(app.config)

    # Apply authentication to the forecast blueprint
    @forecast_blueprint.before_request
    @auth.login_required
    def before_forecast():
        pass

    # Register Blueprints
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(forecast_blueprint, url_prefix='/forecast')

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'error_code': 'not_found'}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled Exception: {error}")
        return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
