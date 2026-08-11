# Hand Gesture Mouse

This project implements a hand-gesture-controlled virtual mouse using your webcam. It lets you move the cursor, click, scroll, and perform simple interactions using intuitive hand gestures — no physical mouse required.

## Overview

The application uses a webcam to detect the user's hand and landmarks (e.g., finger tips) and maps specific gestures to mouse actions. Typical components:

- Hand detection and landmark estimation (MediaPipe Hands or a similar model)
- Video capture and processing (OpenCV)
- Gesture interpretation and state handling
- System control for the mouse and keyboard events (PyAutoGUI or OS-specific libraries)

## Features

- Cursor movement driven by your index finger position
- Left click using a pinching gesture or specific finger combination
- Right click and double-click gestures (optional)
- Scrolling gestures (two-finger movement or tilt)
- Calibration and smoothing to make pointer movement stable and natural

## How it works (high level)

1. Capture frames from the webcam.
2. Run hand landmark detection on each frame to locate fingers and joints.
3. Use landmark positions to determine the gesture (e.g., which fingers are up, distance between thumb and index finger).
4. Map the interpreted gesture to a mouse event (move, click, scroll) and perform the action via an automation library.
5. Provide optional visual feedback (overlay the hand landmarks and the active gesture) on the video feed.

## Requirements

- Python 3.8+
- Webcam

Python packages (install via pip):

- opencv-python
- mediapipe (or another hand-tracking model you're using)
- pyautogui
- numpy

Example:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

Note: On some operating systems, pyautogui may need additional permissions (e.g., accessibility permissions on macOS).

## Installation

1. Clone the repository:

```bash
git clone https://github.com/sahilmisalwar/Hand-gesture-mouse.git
cd Hand-gesture-mouse
```

2. Create a virtual environment (recommended) and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt  # if present, or install packages manually
```

## Usage

Run the main script (replace with the actual entrypoint file in this repo, e.g., `main.py` or `app.py`):

```bash
python main.py
```

While running, the application will open a webcam window showing detected hand landmarks and an overlay that indicates the current gesture and mapped mouse action.

## Gesture mapping (example)

- Move: Move index finger — the cursor follows the index fingertip.
- Left click: Thumb and index finger pinch (distance below threshold).
- Right click: Index and middle finger held in a specific pose (or two-finger tap).
- Scroll: Two-finger vertical movement or swipe up/down.

Adjust thresholds and smoothing parameters in the code for better responsiveness.

## Calibration and tuning

- Use a well-lit environment to improve detection reliability.
- Adjust smoothing factor to trade off between responsiveness and stability.
- Provide a calibration mode if needed (map the camera frame to screen coordinates).

## Troubleshooting

- No webcam detected: ensure your camera is connected and accessible.
- Unstable cursor: increase smoothing or reduce sensitivity.
- Gestures not recognized: check the model dependency (MediaPipe) is installed and up to date.
- Permission errors (macOS): grant accessibility/control permissions to Python or your terminal app.

## Contributing

Contributions are welcome. Suggested ways to improve:

- Add configuration for gesture-to-action mapping
- Add GUI for calibration
- Improve gesture detection robustness
- Add tests and CI

Please open issues or pull requests on GitHub.

## License

Specify a license for your project (e.g., MIT). Add a LICENSE file to this repository if needed.
