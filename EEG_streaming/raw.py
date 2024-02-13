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

channel_names = [
    'CP3', 'C3',
    'F5',  'PO3',
    'PO4', 'F6',
    'C4',  'CP4'
]

def callback(data):
    print("Received data")
    append_to_csv(data["data"], data["info"]["startTime"])

def append_to_csv(data, start_time):
    # Transpose the data to have each channel in a separate column
    transposed_data = list(map(list, zip(*data)))

    with open(csv_file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write channel names and start time as the header
        writer.writerow(channel_names + ["StartTime"])
        
        # Write the transposed data and start time to the CSV file
        writer.writerows([*transposed_data, [start_time]])
        
unsubscribe = neurosity.brainwaves_raw(callback)

