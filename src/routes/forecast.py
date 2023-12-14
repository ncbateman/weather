# routes/forecast.py

from flask import Blueprint, jsonify, request, current_app
from services.weather_service import WeatherService

# Create a Blueprint for the forecast route
forecast_blueprint = Blueprint('forecast', __name__)

@forecast_blueprint.route('/<city>/', methods=['GET'])
def get_forecast(city):
    """
    Endpoint to get the weather forecast for a specific city.
    Optionally, a date or datetime can be provided in the query string
    in ISO 8601 format.
    """
    weather_service = WeatherService(current_app.config)
    
    # Optional: Handle 'at' query parameter for specific date or datetime
    forecast_date = request.args.get('at', None)

    try:
        if forecast_date:
            # If a specific date is provided, fetch forecast for that date
            # Implement the logic based on your requirements
            # For example, weather_service.get_forecast_by_date(city, forecast_date)
            pass
        else:
            # Fetch current weather data
            weather_data = weather_service.get_weather_data(city)
        return jsonify(weather_data)
    except Exception as e:
        # Handle exceptions and errors
        return jsonify({'error': str(e)}), 500

