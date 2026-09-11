import pulsectl

def get_volume() -> float:
    with pulsectl.Pulse('volume-daemon') as pulse:
        sink = pulse.sink_default_get()
        return pulse.volume_get_all_chans(sink)

def set_volume(volume: float):
    with pulsectl.Pulse('volume-daemon') as pulse:
        sink = pulse.sink_default_get()
        pulse.volume_set_all_chans(sink, max(0.0, min(1.0, volume)))