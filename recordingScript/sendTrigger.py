import time
import threading
from pylsl import StreamInfo, StreamOutlet


def send_trigger():
    info = StreamInfo(name='TriggerStream', type='Markers', channel_count=1,
                 nominal_srate=0, channel_format='string')
    outlet = StreamOutlet(info)
    counter = 0
    while True:
        print(f"Sending trigger {counter}")
        outlet.push_sample([f'Trigger {counter}'])
        counter += 1
        time.sleep(5)

# Run everything
try:
    trigger_thread = threading.Thread(target=send_trigger)
    trigger_thread.start()

    print("Recording... Press Ctrl+C to stop.")
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")
