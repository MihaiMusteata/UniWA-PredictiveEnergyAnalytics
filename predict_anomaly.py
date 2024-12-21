import pandas as pd
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib

# Define a function to predict and detect anomalies
def predict_and_detect_anomalies(file_name, machine_name, data):
    if os.path.exists(file_name):
        # Load the file
        df = pd.read_csv(file_name)

        # Load the pre-trained model
        model_file = f"{machine_name}_optimized_model.pkl"
        if not os.path.exists(model_file):
            print(f"Model file {model_file} not found. Skipping.")
            return {
                "error": f"Model file {model_file} not found."
            }

        # Load the model
        model = joblib.load(model_file)

        X_next = pd.DataFrame([data])
        # Predict energy consumption for the next hour
        predicted_consumption = model.predict(X_next)[0]

        # Add prediction to the dataset
        new_row = {
            'timestamp': data['timestamp'],
            'energy_consumption_kwh': predicted_consumption,
            'temperature_celsius': data['temperature_celsius'],
            'production_rate': data['production_rate'],
            'operating_status': data['operating_status'],
            'downtime_minutes': data['downtime_minutes'],
            'load_factor': data['load_factor'],
            'humidity_percent': data['humidity_percent'],
            'maintenance_alert': data['maintenance_alert'],
        }

        # Append the new row to the dataframe
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Scale data for anomaly detection
        scaler = StandardScaler()
        features_to_scale = ['energy_consumption_kwh', 'temperature_celsius', 'humidity_percent',
                             'downtime_minutes', 'load_factor', 'production_rate']
        scaled_data = scaler.fit_transform(df[features_to_scale])

        # Train Isolation Forest for anomaly detection (only once per machine)
        anomaly_detector = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        df['anomaly_score'] = anomaly_detector.fit_predict(scaled_data)
        df['anomaly'] = df['anomaly_score'].apply(lambda x: 1 if x == -1 else 0)

        # Check if the prediction is an anomaly
        is_anomalous = df.iloc[-1]['anomaly'] == 1
        result_anomaly = "Is something anomalous" if is_anomalous else "Nothing anomalous detected."

        return {
            "predicted_energy_consumption": f"{predicted_consumption:.2f}",
            "anomaly": result_anomaly,
            "is_anomalous": 1 if is_anomalous else 0
        }
    else:
        return {
            "error": f"Data file {file_name} not found."
        }



def run_anomaly_detection(machine_name, data):
    print(f"Running anomaly detection for {machine_name}...")
    file_name = f"{machine_name}.csv"
    return predict_and_detect_anomalies(file_name, machine_name, data)
