from flask import Flask, request, jsonify
from weather import get_weather_data
from predict_anomaly import run_anomaly_detection
import pandas as pd
from flask_cors import CORS
from datetime import datetime, timedelta

app = Flask(__name__)


# Load the dataset
conveyor_belt_data = pd.read_csv("Conveyor_Belt.csv")
packaging_machine_data = pd.read_csv("Packaging_Machine.csv")
sorting_robot_data = pd.read_csv("Sorting_Robot.csv")
cooling_system_data = pd.read_csv("Cooling_System.csv")
forklift_data = pd.read_csv("Forklift.csv")

CORS(app)


@app.route('/data', methods=['GET'])
def get_data():
    machine_name = request.args.get('machine_name')
    number_of_hours = request.args.get('number_of_hours')

    dataset = None
    if machine_name == 'Conveyor_Belt':
        dataset = conveyor_belt_data
    elif machine_name == 'Packaging_Machine':
        dataset = packaging_machine_data
    elif machine_name == 'Sorting_Robot':
        dataset = sorting_robot_data
    elif machine_name == 'Cooling_System':
        dataset = cooling_system_data
    elif machine_name == 'Forklift':
        dataset = forklift_data
    else:
        return jsonify({"error": "Invalid machine name."}), 400

    dataset['timestamp'] = pd.to_datetime(dataset['timestamp'])

    now = datetime.now().replace(microsecond=0)

    time_ago = now - timedelta(hours=int(number_of_hours))

    filtered_data = dataset[(dataset['timestamp'] >= time_ago) & (dataset['timestamp'] <= now)]

    return filtered_data.to_json(orient='records'), 200


@app.route('/predict-anomaly', methods=['POST'])
def predict_anomaly():
    try:
        # Parse input data from the request
        data = request.json

        # Extract required fields from the request
        machine_name = data.get('machine_name')
        operating_status = data.get('operating_status')

        # Get weather data
        weather_data = get_weather_data()
        if not weather_data:
            return jsonify({"error": "Failed to retrieve weather data."}), 500

        temperature_celsius = weather_data['temperature_celsius']
        humidity_percent = weather_data['humidity_percent']
        weather_condition = weather_data['weather_condition']
        next_hour = pd.Timestamp.now().replace(minute=0, second=0, microsecond=0) + pd.Timedelta(hours=1)

        # Construct input dataframe for prediction
        input_data = {
            'timestamp': next_hour.timestamp(),
            'temperature_celsius': temperature_celsius,
            'production_rate': 100,  # Example production rate
            'operating_status': operating_status,
            'humidity_percent': humidity_percent,
            'downtime_minutes': 0,  # No downtime
            'load_factor': 0.75,  # Example load factor
            'maintenance_alert': operating_status == 2  # Maintenance alert if status is 'Maintenance'
        }

        response = run_anomaly_detection(machine_name, input_data)
        print(response)
        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/weather', methods=['GET'])
def get_weather():
    weather_data = get_weather_data()
    if not weather_data:
        return jsonify({"error": "Failed to retrieve weather data."}), 500

    return jsonify(weather_data), 200

if __name__ == '__main__':
    app.run(debug=True)
