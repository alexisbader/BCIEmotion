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
csv_file_path = "raw_data.csv"

def callback(data):
    print("Received data")

    # Flatten the data
    flat_data = [data['label']] + [item for sublist in data['data'] for item in sublist]
    flat_data += [data['info']['notchFrequency'], data['info']['samplingRate'], data['info']['startTime']]
    flat_data += data['info']['channelNames']

    # CSV header
    header = ['label'] + [f'data_{i}' for i in range(len(flat_data) - 4)] + ['notchFrequency', 'samplingRate', 'startTime'] + data['info']['channelNames']

    # Write to CSV in append mode
    with open('raw_data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Check if the file is empty, then write the header
        if os.stat('raw_data.csv').st_size == 0:
            csv_writer.writerow(header)
        csv_writer.writerow(flat_data)
        
unsubscribe = neurosity.brainwaves_raw(callback)

