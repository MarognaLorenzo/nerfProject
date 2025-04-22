import time
import threading
import explorepy
from explorepy import core
from pylsl import StreamInlet, resolve_stream
import csv

# Function to save EEG data to a list
eeg_data_list = []

def on_eeg_sample(packet):
    # packet is an ExplorePacket with EEG data
    data = packet.get_data()
    timestamp = packet.get_timestamp()
    eeg_data_list.append([timestamp] + data.tolist())

# Setup ExplorePy EEG stream
def start_explore_eeg():
    explore = core.Explore()
    explore.connect(device_name='Explore_XXXX')  # Replace with your device name
    explore.set_eeg_handler(on_eeg_sample)
    explore.start_acquisition()

# Setup fNIRS stream (assuming Aurora sends LSL data)
fnirs_data_list = []

def start_fnirs_recording():
    print("Resolving fNIRS stream...")
    streams = resolve_stream('type', 'NIRS')  # Change 'NIRS' if Aurora uses a different type
    inlet = StreamInlet(streams[0])
    
    while True:
        sample, timestamp = inlet.pull_sample()
        fnirs_data_list.append([timestamp] + sample)
        time.sleep(0.01)

# Save data to CSV
def save_data():
    with open('eeg_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp'] + [f'EEG_{i}' for i in range(len(eeg_data_list[0]) - 1)])
        writer.writerows(eeg_data_list)

    with open('fnirs_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp'] + [f'fNIRS_{i}' for i in range(len(fnirs_data_list[0]) - 1)])
        writer.writerows(fnirs_data_list)

# Run everything
try:
    eeg_thread = threading.Thread(target=start_explore_eeg)
    fnirs_thread = threading.Thread(target=start_fnirs_recording)

    eeg_thread.start()
    fnirs_thread.start()

    print("Recording... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping and saving...")
    save_data()
