import csv
from neurosity import NeurositySDK
from dotenv import load_dotenv
import os

load_dotenv()

neurosity = NeurositySDK({
    "device_id": os.getenv("NEUROSITY_DEVICE_ID"),
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

# Define the CSV file path
csv_file_path = "power_by_band_data.csv"

def callback(data):
    print("Received data")

    # Flatten the data
    flat_data = [data['label']] + [item for sublist in data['data'].values() for item in sublist]

    # CSV header
    header = ['label'] + [f'{band}_{i}' for band in data['data'].keys() for i in range(len(data['data'][band]))]

    # Write to CSV in append mode
    with open('power_by_band_data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Check if the file is empty, then write the header
        if os.stat('power_by_band_data.csv').st_size == 0:
            csv_writer.writerow(header)
        csv_writer.writerow(flat_data)
        
unsubscribe = neurosity.brainwaves_power_by_band(callback)

