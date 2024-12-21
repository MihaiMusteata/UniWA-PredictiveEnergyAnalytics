import pandas as pd

# Legend for mapping machine_name integers to machine names
machine_legend = {
    0: 'Conveyor_Belt',
    1: 'Packaging_Machine',
    2: 'Sorting_Robot',
    3: 'Cooling_System',
    4: 'Forklift'
}

# Load the dataset
dataset_file = "processed_dataset.csv"
df = pd.read_csv(dataset_file)

# Process the dataset and split by machine_name
for machine_id, machine_name in machine_legend.items():
    # Filter rows for the current machine_name
    machine_data = df[df['machine_name'] == machine_id]

    # Drop the 'machine_name' column
    machine_data = machine_data.drop(columns=['machine_name'])

    # Save to a separate CSV file
    output_file = f"{machine_name}.csv"
    machine_data.to_csv(output_file, index=False)

    print(f"Data for {machine_name} saved to {output_file}")
