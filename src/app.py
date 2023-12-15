from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from services.weather_service import WeatherService
from routes.ping import ping_blueprint
from routes.forecast import forecast_blueprint
from utils.config import Config
import os
import yaml

# Define the root directory of the application. This is used for configuration file loading.
WEATHER_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app(testing=False):
    """
    Initialize and configure the Flask application.

    Args:
        testing (bool): If True, the app will be configured for testing.

    Returns:
        Flask app: The configured Flask application.
    """

    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # Load configuration using Config singleton
    config_instance = Config.get_instance()
    config_instance.load_app_config(testing)
    config_instance.load_user_credentials()
    
    # Load config into app
    app.config.update(config_instance.get_app_config())

    # Initialize WeatherService and other services
    weather_service = WeatherService(config_instance)

    # Register Blueprints
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(forecast_blueprint, url_prefix='/forecast')

    # Define error handlers for different HTTP errors.
    @app.errorhandler(404)
    def not_found(error):
        """Return a custom JSON response for 404 Not Found errors."""
        return jsonify({'error': 'Not found', 'error_code': 'not_found'}), 404

    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handle uncaught exceptions and log them."""
        app.logger.error(f"Unhandled Exception: {error}")
        return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500

    return app

if __name__ == '__main__':
    # Run the application if the script is executed directly.
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8080)
