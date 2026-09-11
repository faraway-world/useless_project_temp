# Thermal Volume Prank

A dynamic daemon that monitors audio volume and system temperature to orchestrate an escalating series of stressful events, ending in an unkillable Rickroll lock screen.

## Features

- **Head Tracking Volume Control**: Modulate your system's audio volume just by turning your head left or right (powered by MediaPipe and OpenCV).
- **Thermal Stressing**: If the volume goes above 60%, the script automatically spins up CPU and GPU stress tests (`mprime` and `glmark2`) to heat up the chassis.
- **Critical Thermal Warning**: When the chassis temperature hits 85°C, a GTK-based warning overlay appears.
- **Unkillable Rickroll**: If the warning is ignored (override is clicked or 10 seconds pass), the daemon locks the screen with a transparent input blocker and blasts a looping Rickroll at maximum volume.
- **Kill Sequence**: The Rickroll can only be stopped by entering the secret kill sequence (`Ctrl + Super + Alt + Space`).

## Prerequisites

### System Requirements

This project relies on some system-level binaries and libraries for its functions. You will need to install the following on your Linux system:

- **GTK 3 & GTK Layer Shell**: For drawing the warning overlay and lock screen.
- **mprime & glmark2**: For stressing the CPU and GPU.
- **mpv**: For playing the Rickroll video (`rickroll.mp4`).

Example for Arch-based systems:
```bash
sudo pacman -S gtk3 gtk-layer-shell mprime glmark2 mpv
```

### Python Dependencies

The required Python packages are listed in `requirements.txt`. Install them using:
```bash
pip install -r requirements.txt
```

## Running the Daemon

Ensure you have the `face_landmarker.task` model file (for MediaPipe) and `rickroll.mp4` in the project root.

Run the main daemon:
```bash
python linux/main.py
```

## How It Works

1. **Normal State**: Normal operation. Head tracking works to adjust volume.
2. **Heating State**: Volume > 60%. CPU/GPU stress starts to generate heat.
3. **Warning State**: Temperature >= 85.0°C. An overlay is displayed.
4. **Countdown/Prank State**: User ignores the warning, triggering a 10s countdown followed by an infinite Rickroll with an input-blocking screen.

*Note: Proceed at your own risk! This script intentionally generates heat and locks your input.*