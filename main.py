import pandas as pd

df = pd.read_csv("warehouse_energy_consumption.csv")

# Convert categorical columns to numeric representations

# 1. 'machine_name': Map machine names to integers
# Legend:
#   - 'Conveyor Belt' -> 0
#   - 'Packaging Machine' -> 1
#   - 'Sorting Robot' -> 2
#   - 'Cooling System' -> 3
#   - 'Forklift' -> 4
machine_mapping = {
    'Conveyor Belt': 0,
    'Packaging Machine': 1,
    'Sorting Robot': 2,
    'Cooling System': 3,
    'Forklift': 4
}
df['machine_name'] = df['machine_name'].map(machine_mapping)

# 2. 'operating_status': Map statuses to integers
# Legend:
#   - 'Operational' -> 0
#   - 'Idle' -> 1
#   - 'Maintenance' -> 2
status_mapping = {
    'Operational': 0,
    'Idle': 1,
    'Maintenance': 2
}
df['operating_status'] = df['operating_status'].map(status_mapping)

# 3. 'weather_condition': Map weather conditions to integers
# Legend:
#   - 'Clear' -> 0
#   - 'Rain' -> 1
#   - 'Snow' -> 2
#   - 'Cloudy' -> 3
weather_mapping = {
    'Clear': 0,
    'Rain': 1,
    'Snow': 2,
    'Cloudy': 3
}
df['weather_condition'] = df['weather_condition'].map(weather_mapping)

# Save the adjusted dataset to a new CSV file
df.to_csv("processed_dataset.csv", index=False)

# Display the processed dataset
print("Dataset processed and saved as 'processed_dataset.csv'.")
