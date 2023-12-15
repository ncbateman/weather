from flask import Blueprint, jsonify, request, current_app
from services.weather_service import WeatherService
from dateutil.parser import parse
import pytz

# Create a Blueprint for the forecast route
forecast_blueprint = Blueprint('forecast', __name__)

@forecast_blueprint.route('/<city>/', methods=['GET'])
def get_forecast(city):
    weather_service = WeatherService(current_app.config)

    # Convert city to coordinates (latitude, longitude) using the WeatherService
    lat, lon = weather_service.convert_city_to_coordinates(city)
    if lat is None or lon is None:
        return jsonify({'error': f"Cannot find city '{city}'", 'error_code': 'city_not_found'}), 404

    forecast_date = request.args.get('at', None)
    if forecast_date:
        forecast_date = forecast_date.replace(" ", "+")
        try:
            # Convert the ISO 8601 date to a datetime object
            datetime_obj = parse(forecast_date)

            # Ensure both datetime objects are either naive or aware
            if datetime_obj.tzinfo is None or datetime_obj.tzinfo.utcoffset(datetime_obj) is None:
                # Make it an aware datetime object
                datetime_obj = datetime_obj.replace(tzinfo=pytz.UTC)
            compare_date = parse("1979-01-01").replace(tzinfo=pytz.UTC)

            # Check if the date is before January 1, 1979
            if datetime_obj < compare_date:
                return jsonify({'error': 'Dates before January 1st, 1979 are not supported', 'error_code': 'invalid_date'}), 400

            # Convert datetime to a timestamp
            timestamp = int(datetime_obj.timestamp())

        except ValueError as e:
            return jsonify({'error': 'Invalid date format', 'error_code': 'invalid_date_format'}), 400
    else:
        timestamp = None

    try:
        # Fetch weather data (current or specific time)
        status_code, data = weather_service.get_weather(lat, lon, timestamp)
        return jsonify(data), status_code
    except Exception as e:
        # Generic catch-all 500 error response
        return jsonify({'error': 'Something went wrong', 'error_code': 'internal_server_error'}), 500

# TODO: add error for too far in the future.
