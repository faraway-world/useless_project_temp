import subprocess
import os
import signal

class StressManager:
    def __init__(self):
        self.procs = []

    def start(self):
        if not self.procs:
            try:
                self.procs.append(
                    subprocess.Popen(
                        ['mprime', '-t'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                )
            except FileNotFoundError:
                pass
            
            try:
                self.procs.append(
                    subprocess.Popen(
                        ['prime-run', 'glmark2', '--off-screen', '--run-forever'],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        start_new_session=True
                    )
                )
            except FileNotFoundError:
                pass

    def stop(self):
        for p in self.procs:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
        self.procs.clear()