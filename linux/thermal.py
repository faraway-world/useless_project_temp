import psutil
from collections import deque

class ThermalMonitor:
    def __init__(self):
        self._temps = deque(maxlen=6)

    def get_smoothed_temp(self) -> float:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            for entry in temps['coretemp']:
                if entry.label == 'Package id 0':
                    self._temps.append(entry.current)
                    break
        
        if not self._temps:
            return 0.0
        return sum(self._temps) / len(self._temps)