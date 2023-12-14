from flask import Flask, jsonify, request
from services.weather_service import WeatherService
from routes.ping import ping_blueprint
from routes.forecast import forecast_blueprint
import os
import yaml

# Define the root directory relative to the current file
WEATHER_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize Flask application
app = Flask(__name__)

# Construct the path to the YAML configuration file
config_path = os.path.join(WEATHER_ROOT_DIR, 'config', 'config.yaml')

# Load configuration from YAML file
with open(config_path, 'r') as config_file:
    config_data = yaml.safe_load(config_file)
    app.config.update(config_data)

# Initialize services
weather_service = WeatherService(app.config)

# Register Blueprints
app.register_blueprint(ping_blueprint)
app.register_blueprint(forecast_blueprint, url_prefix='/forecast')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'error_code': 'not_found'}), 404

@app.errorhandler(Exception)
def handle_exception(error):
    """Handle all unhandled exceptions with a generic error message."""
    app.logger.error(f"Unhandled Exception: {error}")  # Log the error for debugging
    return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
