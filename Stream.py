from pylsl import StreamInfo, StreamOutlet

class Stream(StreamOutlet):
    def __init__(self, active: bool, name="MarkerStream", type="Markers", channel_count=1, nominal_srate=0, channel_format='string'):
        info = StreamInfo(name = name,type = type, channel_count=channel_count, channel_format=channel_format, nominal_srate=nominal_srate)
        super().__init__(info)
        self.active = active
    
    def push_sample(self, x, timestamp = 0, pushthrough = True):
        if not self.active:
            return 
        return super().push_sample(x, timestamp, pushthrough)
    
    def send_marker(self, x: str, timestamp = 0, pushthrough = True):
        return self.push_sample([x], timestamp, pushthrough)