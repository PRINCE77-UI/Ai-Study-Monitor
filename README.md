# 🎓 AI Study Monitor

An AI-powered webcam application that keeps students focused while studying. It watches for three things in real time and raises an instant audio + on-screen alert the moment it catches you:

- 😴 **Sleeping** — detects drowsiness using eye-aspect-ratio (EAR) from facial landmarks
- 📱 **Phone usage** — detects a cell phone in frame using a YOLOv8 object detector
- 🙈 **Covered / hidden face** — detects when your face disappears from the camera for too long

> Every parent wanted this... so I built it 😂

## 🎥 Demo
👉 [Try it live here] (https://ai-study-monitor-lk7cssdqksevmlrrems9y4.streamlit.app/)

## 🛠️ Tech Stack

- **OpenCV** — video capture & rendering
- **cvzone FaceMeshModule** (built on MediaPipe) — facial landmark detection for drowsiness detection
- **Ultralytics YOLOv8** — real-time cell phone detection (COCO pre-trained `yolov8n.pt`)
- **Pygame** — instant audio alerts

## ⚙️ How It Works

1. Captures live webcam feed frame by frame.
2. Runs face-mesh detection to compute the eye-aspect ratio; if eyes stay closed beyond a frame threshold → **sleep alert**.
3. If no face is detected for too many consecutive frames → **face-covered alert**.
4. Runs YOLOv8 on each frame to detect a cell phone with confidence > 0.5 → **phone alert**.
5. Alerts are prioritized (face-covered > sleep > phone) so only one warning plays at a time, with on-screen text and a sound cue.

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/PRINCE77-UI/Ai-Study-Monitor.git
cd Ai-Study-Monitor


Add your own alert sound files inside the folder:
- alarm.mp3 — played on sleep detection
- faudio.mp3 — played on face-covered detection
- paudio.mp3 — played on phone detection

## ▶️ Usage

```bash
python App.py
```

Press `q` to quit the app.

## 📌 Notes

- The first run will auto-download the `yolov8n.pt` YOLOv8 weights via Ultralytics.
- Works best with a well-lit, front-facing webcam setup.
- Thresholds (`SLEEP_THRESHOLD_FRAMES`, `COVER_THRESHOLD_FRAMES`, eye-ratio cutoff) can be tuned in `study_monitor.py` based on your webcam's FPS.

## 👤 Author

**Prince Kumar** — Python Developer

---
If you found this project interesting, consider ⭐ starring the repo!
