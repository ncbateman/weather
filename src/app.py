from flask import Flask, jsonify
from services.weather_service import WeatherService
from routes.ping import ping_blueprint
from routes.forecast import forecast_blueprint
import os
import yaml

def create_app(testing=False):
    # Define the root directory of the application.
    WEATHER_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    # Initialize the Flask application.s
    app = Flask(__name__)

    # Load configuration
    if testing:
        # Load testing configuration
        app.config['TESTING'] = True
        app.config['API_KEY'] = 'test_api_key'
    else:
        config_path = os.path.join(WEATHER_ROOT_DIR, 'config', 'config.yaml')
        with open(config_path, 'r') as config_file:
            config_data = yaml.safe_load(config_file)
            app.config.update(config_data)

    # Initialize WeatherService
    weather_service = WeatherService(app.config)

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
