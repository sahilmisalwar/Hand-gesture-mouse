<div align="center">

# 🖐️ Hand Gesture Controlled Virtual Mouse

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)

</div>

A real-time hand gesture-based virtual mouse controller using a webcam. This system tracks the user's hand using MediaPipe Hands, detects raised fingers using landmark geometry, and maps specific gestures to OS-level mouse actions (move, click, scroll, right-click).

---

## 📑 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Gesture Guide](#-gesture-guide)
- [Configuration](#-configuration)
- [Performance Tips](#-performance-tips)
- [Known Limitations](#-known-limitations)
- [Roadmap / Future Scope](#-roadmap--future-scope)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## ✨ Features
- 🖱️ **Smooth Cursor Control**: Exponential smoothing for jitter-free cursor movement.
- 🖐️ **Accurate Hand Tracking**: Robust hand detection powered by MediaPipe.
- 🤏 **Pinch-to-Click**: Natural pinch gesture for left-clicking with cooldown to prevent spam.
- 📜 **Vertical Scrolling**: Two-finger gesture to scroll up and down smoothly.
- 🖥️ **Live HUD**: Real-time display of FPS, current gesture, and individual finger states.

---

## 🎥 Demo
📸 *Screenshots coming soon*

*(Placeholder for future demo GIF or image showing the HUD and gesture in action)*

---

## 🛠 Tech Stack

| Tool | Purpose | Version |
|---|---|---|
| **Python** | Core Language | 3.8+ |
| **OpenCV** | Webcam capture & HUD drawing | >=4.8.0 |
| **MediaPipe** | Hand tracking & landmark detection | >=0.10.0 |
| **PyAutoGUI** | OS mouse event simulation | >=0.9.54 |
| **NumPy** | Array manipulation | >=1.24.0 |

---

## 🏗 System Architecture

```text
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│   Webcam    │────▶│  hand_tracker.py │────▶│ gesture_controller  │
│  (OpenCV)   │     │  (MediaPipe)     │     │      .py            │
└─────────────┘     └──────────────────┘     └──────────┬──────────┘
                                                         │
                                               Gesture String
                                                         │
                                                         ▼
                                             ┌─────────────────────┐
                                             │  mouse_controller   │
                                             │       .py           │
                                             │   (PyAutoGUI)       │
                                             └──────────┬──────────┘
                                                         │
                                                         ▼
                                             ┌─────────────────────┐
                                             │   OS Mouse Events   │
                                             │ Move / Click / Scroll│
                                             └─────────────────────┘
```

---

## 📁 Project Structure

```text
hand-gesture-mouse/
├── assets/
│   └── screenshots/
│       └── .gitkeep
├── gesture_controller.py   # Gesture logic & cooldowns
├── hand_tracker.py         # MediaPipe tracking & finger states
├── main.py                 # App entry point & main loop
├── mouse_controller.py     # OS mouse interaction & smoothing
├── README.md               # Documentation
└── requirements.txt        # Dependencies
```

---

## 🚀 Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/yourusername/hand-gesture-mouse.git
cd hand-gesture-mouse
```

**Step 2: Create a virtual environment (recommended)**
```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the application**
```bash
python main.py
```

---

## 💻 Usage

1. Ensure your webcam is connected and unblocked.
2. Run `python main.py`.
3. A window titled **"Hand Gesture Mouse | Press Q to quit"** will appear.
4. Position your hand in front of the camera (about 1-2 feet away).
5. Perform gestures to control the mouse.
6. Press `Q` while the webcam window is focused to exit the application.

---

## 🤌 Gesture Guide

| Gesture | Fingers Raised | Action | Notes |
|---|---|---|---|
| ☝️ One Finger | Index only | Move Cursor | Smooth tracking mode |
| ✌️ Two Fingers | Index + Middle | Scroll | Up = scroll down, Down = scroll up |
| 🤏 Pinch | Thumb + Index close | Left Click | 20-frame cooldown |
| 🤟 Three Fingers | Index + Middle + Ring | Right Click | 20-frame cooldown |
| ✋ Other / Palm | Any other combo | No Action | System idle |

---

## ⚙️ Configuration

You can tune the system by modifying these constants in their respective files:

| Parameter | File | Default | Description |
|---|---|---|---|
| `PINCH_THRESHOLD` | `gesture_controller.py` | 40 | Pixel distance for pinch detection |
| `COOLDOWN_FRAMES` | `gesture_controller.py` | 20 | Frames before re-triggering click |
| `smoothing` | `mouse_controller.py` | 0.25 | Cursor smoothing factor (0–1) |
| `detection_confidence` | `hand_tracker.py` | 0.75 | MediaPipe detection confidence |
| `tracking_confidence` | `hand_tracker.py` | 0.75 | MediaPipe tracking confidence |
| `FRAME_WIDTH` | `main.py` | 640 | Webcam capture width |
| `FRAME_HEIGHT` | `main.py` | 480 | Webcam capture height |

---

## ⚡ Performance Tips
- **Lighting**: Ensure your face and hands are well-lit for optimal MediaPipe performance.
- **Background**: A plain, non-cluttered background improves hand tracking reliability.
- **Distance**: Keep your hand approximately 1-2 feet from the webcam.
- **Smoothing**: Increase `smoothing` in `mouse_controller.py` if the cursor feels jittery (values closer to 0 are smoother but laggier, values closer to 1 are instant but jittery).

---

## ⚠️ Known Limitations
- Failsafe is disabled in PyAutoGUI to prevent crashes when moving the cursor to corners, which means you cannot use corner-exit to kill the script. Use `Q` to quit.
- High CPU usage depending on the system due to continuous image processing.
- Hand occlusion or extremely fast movements may cause tracking loss.

---

## 🗺️ Roadmap / Future Scope
- [x] Basic mouse movement and clicking
- [x] Scrolling support
- [ ] Drag and drop support (Pinch and hold)
- [ ] Volume control gesture
- [ ] Multi-hand support (e.g., right hand for mouse, left hand for keyboard shortcuts)
- [ ] Desktop GUI for configuring settings without editing code

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](#) if you want to contribute.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Acknowledgements
- [MediaPipe](https://mediapipe.dev/) for the robust ML hand tracking models.
- [OpenCV](https://opencv.org/) for the real-time computer vision library.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for cross-platform GUI automation.

---
*Generated with Antigravity — Sahil's AI-powered modular build system*
