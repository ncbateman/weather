from flask import Blueprint, jsonify, request, current_app
from services.weather_service import WeatherService
from dateutil.parser import parse
from datetime import datetime as dt, timedelta
from flask_httpauth import HTTPBasicAuth
from utils.config import Config
import os
import pytz
import yaml

# Create a Blueprint for the forecast route
forecast_blueprint = Blueprint('forecast', __name__)

# Update the load_user_credentials function to use the Config class
def load_user_credentials(testing=False):
    config_instance = Config.get_instance()
    config_instance.load_user_credentials()
    return config_instance.get_user_credentials()

users = load_user_credentials()

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username

# Apply authentication to the forecast blueprint
@forecast_blueprint.before_request
@auth.login_required
def before_forecast():
    pass

@forecast_blueprint.route('/<city>/', methods=['GET'])
@forecast_blueprint.route('/<city>/', methods=['GET'])
def get_forecast(city):
    """
    Retrieve the weather forecast for a specified city.

    This endpoint converts a city name to coordinates and then fetches weather data.
    It handles date parsing for specific time forecasts and checks if the requested date 
    is within the allowable range (up to 4 days in the future).

    Args:
        city (str): The name of the city.

    Returns:
        Response: JSON response containing weather data or an error message.
    """
    weather_service = WeatherService(current_app.config)

    # Convert the city name to geographic coordinates.
    lat, lon = weather_service.convert_city_to_coordinates(city)
    if lat is None or lon is None:
        return jsonify({'error': f"Cannot find city '{city}'", 'error_code': 'city_not_found'}), 404

    forecast_date = request.args.get('at', None)
    if forecast_date:
        forecast_date = forecast_date.replace(" ", "+")
        try:
            # Parse the provided date and ensure it's in a valid format.
            datetime_obj = parse(forecast_date)
            if datetime_obj.tzinfo is None or datetime_obj.tzinfo.utcoffset(datetime_obj) is None:
                datetime_obj = datetime_obj.replace(tzinfo=pytz.UTC)
            compare_date = parse("1979-01-01").replace(tzinfo=pytz.UTC)

            if datetime_obj < compare_date:
                return jsonify({'error': 'Dates before January 1st, 1979 are not supported', 'error_code': 'invalid_date'}), 400

            # Check if the date is more than 4 days in the future.
            max_future_date = dt.now(pytz.UTC) + timedelta(days=4)
            if datetime_obj > max_future_date:
                return jsonify({'error': 'Dates more than 4 days in the future are not supported', 'error_code': 'invalid_date'}), 400

            timestamp = int(datetime_obj.timestamp())

        except ValueError:
            return jsonify({'error': 'Invalid date format', 'error_code': 'invalid_date_format'}), 400
    else:
        timestamp = None

    try:
        # Fetch and return the weather data.
        status_code, data = weather_service.get_weather(lat, lon, timestamp)
        return jsonify(data), status_code
    except Exception as e:
        return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500