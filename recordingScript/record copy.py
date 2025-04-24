import time
import threading
import csv


def start_fnirs_recording():
    print("Resolving fNIRS stream...")
    # streams = resolve_stream('type', 'NIRS')  # Change 'NIRS' if Aurora uses a different type
    # inlet = StreamInlet(streams[0])
    
    while True:
        # sample, timestamp = inlet.pull_sample()
        # fnirs_data_list.append([timestamp] + sample)
        time.sleep(0.01)

# Save data to CSV
def save_data():
    eeg_data_list = []
    fnirs_data_list = []
    with open('eeg_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp'] + [f'EEG_{i}' for i in range(len(eeg_data_list[0]) - 1)])
        writer.writerows(eeg_data_list)

    with open('fnirs_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp'] + [f'fNIRS_{i}' for i in range(len(fnirs_data_list[0]) - 1)])
        writer.writerows(fnirs_data_list)




def start_triggers_recording():
    from pylsl import StreamInlet, StreamInfo, resolve_streams
    print("Resolving trigger stream...")

    # Resolve the trigger stream - you can specify more precise parameters if needed
    streams = resolve_streams()  
    if len(streams) == 0:
        raise RuntimeError("No trigger stream found")
    inlet = StreamInlet(streams[0])


    while True:
        sample, timestamp = inlet.pull_sample()
        print(f"Received trigger: {sample[0]} at time {timestamp}")
        time.sleep(0.01)


# Run everything
try:
    # eeg_thread = threading.Thread(target=start_explore_eeg)
    # fnirs_thread = threading.Thread(target=start_fnirs_recording)
    trigger_thread = threading.Thread(target=start_triggers_recording)

    # eeg_thread.start()
    # fnirs_thread.start()
    trigger_thread.start()

    print("Recording... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping and saving...")
    save_data()
