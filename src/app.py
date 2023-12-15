from flask import Flask, jsonify, request
from services.weather_service import WeatherService
from routes.ping import ping_blueprint
from routes.forecast import forecast_blueprint
import os
import yaml

# Define the root directory of the application.
# This is the directory where this script is located.
WEATHER_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Initialize the Flask application.
# This instance of Flask will handle all the routes and requests.
app = Flask(__name__)

# Construct the path to the configuration file.
# The configuration file is expected to be in the 'config' folder under the root directory.
config_path = os.path.join(WEATHER_ROOT_DIR, 'config', 'config.yaml')

# Open and read the YAML configuration file.
# YAML files are used for configuration because they are human-readable and easy to edit.
with open(config_path, 'r') as config_file:
    config_data = yaml.safe_load(config_file)  # Load the YAML content into a Python dictionary.
    app.config.update(config_data)  # Update the Flask app's configuration with this data.

# Initialize external services required by the app.
# In this case, we're initializing a weather service with configuration from the app.
weather_service = WeatherService(app.config)

# Register Blueprints for different parts of the application.
# Blueprints help organize the application into distinct components.
app.register_blueprint(ping_blueprint)  # Blueprint for handling 'ping' requests.
app.register_blueprint(forecast_blueprint, url_prefix='/forecast')  # Blueprint for weather forecast related routes.

# Error handler for 404 Not Found errors.
# This function returns a JSON response with an error message and code when a 404 error occurs.
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found', 'error_code': 'not_found'}), 404

# Global error handler for unhandled exceptions.
# Catches any exceptions not explicitly handled in the routes and returns a generic error response.
@app.errorhandler(Exception)
def handle_exception(error):
    app.logger.error(f"Unhandled Exception: {error}")  # Log the error for debugging purposes.
    return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500

# The main entry point of the application.
# Checks if this script is being run directly (not imported) and then starts the Flask server.
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)  # Run the application with debugging enabled on port 8080.
