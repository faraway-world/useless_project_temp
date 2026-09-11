import sys
import time
import subprocess
from enum import Enum, auto

import audio
from thermal import ThermalMonitor
from stress import StressManager
from head_tracker import HeadTracker

class State(Enum):
    NORMAL = auto()
    HEATING = auto()
    WARNING = auto()
    COUNTDOWN = auto()
    PRANK = auto()

def main():
    monitor = ThermalMonitor()
    stress_mgr = StressManager()

    def volume_callback(delta: float):
        current = audio.get_volume()
        audio.set_volume(current + delta)

    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    model_path = os.path.join(root_dir, 'face_landmarker.task')

    tracker = HeadTracker(volume_callback, model_path=model_path)
    tracker.start()

    state = State.NORMAL
    countdown_until = 0.0
    overlay_proc = None

    try:
        while True:
            now = time.time()
            current_vol = audio.get_volume()
            temp = monitor.get_smoothed_temp()

            if state == State.NORMAL:
                if current_vol > 0.60:
                    state = State.HEATING
                    stress_mgr.start()

            elif state == State.HEATING:
                if current_vol <= 0.60:
                    stress_mgr.stop()
                    state = State.NORMAL
                elif temp >= 85.0:
                    state = State.WARNING
                    overlay_path = os.path.join(base_dir, 'overlay.py')
                    overlay_proc = subprocess.Popen([sys.executable, overlay_path])

            elif state == State.WARNING:
                if overlay_proc:
                    ret = overlay_proc.poll()
                    if ret == 0:
                        audio.set_volume(0.60)
                        stress_mgr.stop()
                        state = State.NORMAL
                    elif ret == 1:
                        countdown_until = now + 10.0
                        state = State.COUNTDOWN

            elif state == State.COUNTDOWN:
                if current_vol <= 0.60:
                    stress_mgr.stop()
                    state = State.NORMAL
                elif now >= countdown_until:
                    state = State.PRANK

            elif state == State.PRANK:
                # Keep the fire burning
                stress_mgr.start()
                audio.set_volume(1.0)
                
                rickroll_path = os.path.join(root_dir, 'rickroll.mp4')
                # Launch Rickroll looping infinitely
                mpv_proc = subprocess.Popen(
                    ['mpv', '--fs', '--no-terminal', '--ontop', '--loop=inf', '--volume-max=200', '--volume=150', rickroll_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Give mpv a second to map its window before locking over it
                time.sleep(1.0)
                
                lock_path = os.path.join(base_dir, 'lock_screen.py')
                # Deploy the transparent input-blocking wall
                lock_proc = subprocess.Popen([sys.executable, lock_path])
                
                # The daemon halts here until the user inputs the kill sequence (Ctrl+Super+Alt+Space)
                lock_proc.wait()
                
                # Terminate the video once the lock is broken
                if mpv_proc.poll() is None:
                    mpv_proc.terminate()
                
                # Cleanup and kill the daemon
                audio.set_volume(0.60)
                sys.exit(0)

            time.sleep(0.5)

    except KeyboardInterrupt:
        pass
    finally:
        tracker.stop()
        stress_mgr.stop()
        if overlay_proc and overlay_proc.poll() is None:
            overlay_proc.terminate()

if __name__ == "__main__":
    main()