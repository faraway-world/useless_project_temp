# Thermal Volume Daemon

A Linux/Wayland daemon that physically enforces system volume limits by tying audio output to CPU temperature. 

If the volume gets too loud, the daemon intentionally overheats the computer using background stress tests. If the resulting thermal warnings are ignored by user, it locks all user inputs and executes[...]

## Demonstration

https://github.com/user-attachments/assets/78b47b6c-7f92-4a90-837e-8868ff04cf1d


## Features
* **Head-Tracking Volume Control:** Adjust volume by turning your head left or right using webcam tracking (OpenCV + MediaPipe).
* **Artificial Thermal Loading:** Automatically launches `mprime` (CPU) and `glmark2` (GPU) when volume exceeds 60% to rapidly heat the chassis.
* **Wayland-Native Overlay:** Uses GTK Layer Shell to render a critical thermal warning over all active windows.
* **Input-Locking Trap:** If the user overrides the warning, the daemon deploys a transparent GTK wall to absorb all mouse clicks, requests Wayland exclusive keyboard mode, maxes the volume to 150%, a[...]

## Requirements
* **OS:** Linux (Wayland compositors. Tested on Hyprland).
* **System Packages:** `mpv`, `mprime-bin` (AUR), `glmark2`, `gtk-layer-shell`, `python-gobject`
* **Python Packages:** `pulsectl`, `psutil`, `opencv-python`, `mediapipe`

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/faraway-world/thermal-volume.git
   cd thermal-volume
   ```

2. Create a virtual environment with system-site-packages enabled (required for GTK bindings):
   ```bash
   python -m venv --system-site-packages venv
   ```

3. Install the Python dependencies:
   ```bash
   ./venv/bin/pip install pulsectl psutil opencv-python mediapipe
   ```

4. Download the MediaPipe Face Landmarker model:
   ```bash
   wget -O face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
   ```

5. Place a video file named `rickroll.mp4` in the project root directory.
6. Execute the daemon:
   ```bash
   ./venv/bin/python linux/main.py
   ```

## Emergency Escape Hatch

If the daemon enters the `PRANK` state, standard inputs are blocked.

Press **`Ctrl + Super + Alt + Space`** to trigger the kill sequence. This destroys the transparent GTK lock screen, terminates the video, kills all background stress testing, drops the volume back to [...]
