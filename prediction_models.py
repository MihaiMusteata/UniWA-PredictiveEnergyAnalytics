import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
import joblib

# List of machine names and their corresponding file names
machine_names = ['Conveyor_Belt', 'Packaging_Machine', 'Sorting_Robot', 'Cooling_System', 'Forklift']

# Generate a heatmap for each file and train a machine learning model
for machine_name in machine_names:
    file_name = f"{machine_name}.csv"
    if os.path.exists(file_name):
        # Load the file
        df = pd.read_csv(file_name)

        # Convert 'timestamp' to a numerical representation if it exists
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp']).astype(
                int) / 10 ** 9  # Convert to Unix timestamp in seconds

        if {'energy_consumption_kwh', 'temperature_celsius', 'production_rate', 'operating_status', 'humidity_percent', 'downtime_minutes', 'load_factor', 'maintenance_alert'}.issubset(df.columns):

            # Define features and target
            features = ['timestamp', 'temperature_celsius', 'production_rate', 'operating_status', 'humidity_percent', 'downtime_minutes', 'load_factor', 'maintenance_alert']
            target = 'energy_consumption_kwh'

            X = df[features]
            y = df[target]

            # Split the data into training and testing sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Optimize Random Forest Regressor using GridSearchCV
            rf = RandomForestRegressor(random_state=42)
            param_grid = {
                'n_estimators': [100, 200, 300, 400],
                'max_depth': [10, 20, 30, None],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2, 4],
            }
            grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring='neg_mean_squared_error',
                                       n_jobs=-1)
            grid_search.fit(X_train, y_train)

            # Select the best model
            best_model = grid_search.best_estimator_
            print(f"Best parameters for {machine_name}: {grid_search.best_params_}")

            # Evaluate the optimized model
            y_pred = best_model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            print(f"Optimized Mean Squared Error for {machine_name}: {mse:.2f}")

            # Save the trained model
            model_filename = f"{machine_name}_optimized_model.pkl"
            joblib.dump(best_model, model_filename)
            print(f"Trained model for {machine_name} saved as {model_filename}.")

            # Predict for the next hour (example predefined data)
            predefined_data = {
                'timestamp': pd.Timestamp.now().timestamp() + 3600,  # One hour ahead
                'temperature_celsius': 25.0,  # Example temperature
                'production_rate': 100,  # Example production rate
                'operating_status': 0,  # Operational
                'humidity_percent': 50.0,  # Example humidity
                'downtime_minutes': 0,  # No downtime
                'load_factor': 0.75,  # Example load factor
                'maintenance_alert': 0  # Example maintenance alert
            }

            X_next = pd.DataFrame([predefined_data])
            next_prediction = best_model.predict(X_next)
            print(f"Predicted energy consumption for {machine_name} for the next hour: {next_prediction[0]:.2f} kWh")

        else:
            print(f"Insufficient data columns for training in {file_name}.")
    else:
        print(f"File {file_name} does not exist.")
