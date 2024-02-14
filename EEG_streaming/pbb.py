import csv
import time
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

# Constants
NEUTRAL_DURATION = 12  # seconds
EMOTION_DURATION = 46  # seconds
CYCLES = 4  # number of cycles

state = "neutral"

def callback(data):
    print("Received data")

    # Flatten the data
    flat_data = [data['label']] + [item for sublist in data['data'].values() for item in sublist]

    # Add a column for the state ('neutral' or 'emotion')
    flat_data.insert(0, 'neutral' if state == 'neutral' else 'emotion')

    # CSV header
    header = ['state'] + ['label'] + [f'{band}_{i}' for band in data['data'].keys() for i in range(len(data['data'][band]))]

    # Write to CSV in append mode
    with open('power_by_band_data.csv', 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        # Check if the file is empty, then write the header
        if os.stat('power_by_band_data.csv').st_size == 0:
            csv_writer.writerow(header)
        csv_writer.writerow(flat_data)

# Repeat the cycle for the specified number of times
for cycle in range(CYCLES):
    print(f"Cycle {cycle + 1}/{CYCLES}")

    # Collect 'neutral' data
    state = "neutral"
    print("Collecting neutral data...")
    unsubscribe_neutral = neurosity.brainwaves_power_by_band(callback)
    time.sleep(NEUTRAL_DURATION)
    unsubscribe_neutral()

    # Collect 'emotion' data
    state = "emotion"
    print("Collecting emotion data...")
    unsubscribe_emotion = neurosity.brainwaves_power_by_band(callback)
    time.sleep(EMOTION_DURATION)
    unsubscribe_emotion()

# Logout and stop the script
neurosity.logout()
