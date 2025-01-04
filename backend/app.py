from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/weather')
def get_weather():
    url = 'https://dobrapogoda24.pl/api/v1/weather/simple?city=warszawa&day=1&token=d21cbfc6141eaa3c1b71'
    response = requests.get(url)
    data = response.json()

    formatted_data = {
        "date": data["date"],
        "sunrise": data["sunrise"],
        "sunset": data["sunset"],
        "day": {
            "temp_max": f"{data['day']['temp_max']}°C",
            "temp_min": f"{data['day']['temp_min']}°C",
            "felt_temp_max": f"{data['day']['temp_felt_max']}°C",
            "felt_temp_min": f"{data['day']['temp_felt_min']}°C",
            "humidity": f"{data['day']['humidity']}%",
            "pressure": f"{data['day']['pressure']} hPa",
            "wind_speed": f"{data['day']['wind_velocity']} km/h",
            "wind_direction": data['day']['wind_direction']
        },
        "night": {
            "temp_max": f"{data['night']['temp_max']}°C",
            "temp_min": f"{data['night']['temp_min']}°C",
            "felt_temp_max": f"{data['night']['temp_felt_max']}°C",
            "felt_temp_min": f"{data['night']['temp_felt_min']}°C",
            "snow_precipitation": f"{data['night']['precipitation_snow']} mm",
            "wind_speed": f"{data['night']['wind_velocity']} km/h",
            "wind_direction": data['night']['wind_direction']
        }
    }

    return jsonify(formatted_data)

if __name__ == '__main__':
    app.run(debug=True)
