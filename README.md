# 🎓 AI Study Monitor

An AI-powered webcam application that keeps students focused while studying. It watches for three things in real time and raises an instant alert the moment it catches you:

- 😴 **Sleeping** — detects drowsiness using eye-aspect-ratio (EAR) from facial landmarks
- 📱 **Phone usage** — detects a cell phone in frame using a YOLOv8 object detector
- 🙈 **Covered / hidden face** — detects when your face disappears from the camera for too long

> Every parent wanted this... so I built it 😂

## 🔗 Live Demo

👉 **[Try it live in your browser](https://ai-study-monitor-lk7cssdqksevmlrrems9y4.streamlit.app/)** — no install needed, just allow camera access.

*(Runs on free hosting, so it may take a few seconds to load on first visit.)*

## 🎥 Video Demo

📺 **[Watch the demo video]()**

## 🛠️ Tech Stack

- **OpenCV** — video capture & rendering
- **MediaPipe FaceMesh** (via cvzone) — facial landmark detection for drowsiness detection
- **Ultralytics YOLOv8** — real-time cell phone detection (COCO pre-trained `yolov8n.pt`)
- **Pygame** — instant audio alerts (desktop version only)
- **Streamlit + streamlit-webrtc** — browser-based live demo

## ⚙️ How It Works

1. Captures live webcam feed frame by frame.
2. Runs face-mesh detection to compute the eye-aspect ratio; if eyes stay closed beyond a frame threshold → **sleep alert**.
3. If no face is detected for too many consecutive frames → **face-covered alert**.
4. Runs YOLOv8 on each frame to detect a cell phone with confidence > 0.5 → **phone alert**.
5. Alerts are prioritized (face-covered > sleep > phone) so only one warning shows at a time, with on-screen text (and sound in the desktop version).

This repo has two ways to run it:

| Version | File | Camera access | Audio alerts |
|---|---|---|---|
| 🖥️ Desktop app | `app.py` | Local webcam via OpenCV | ✅ Yes (pygame) |
| 🌐 Web app | `streamlit_app.py` | Browser webcam via WebRTC | ❌ Visual only |

## 📦 Installation (Desktop version)

```bash
git clone https://github.com/<your-username>/ai-study-monitor.git
cd ai-study-monitor
pip install -r requirements.txt
```

Add your own alert sound files inside the folder:
- alarm.mp3 — played on sleep detection
- faudio.mp3 — played on face-covered detection
- paudio.mp3 — played on phone detection

Run it:
```bash
python app.py
```
Press `q` to quit.

## 🌐 Running the Web Version Locally

```bash
streamlit run streamlit_app.py
```

## ☁️ Deploying the Web Version Yourself

1. Push this repo to your own GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select this repo → set main file to `streamlit_app.py` → **Deploy**.
4. Make sure `packages.txt` and `requirements.txt` are present at the repo root (already included here).

## 📌 Notes

- The first run auto-downloads the `yolov8n.pt` YOLOv8 weights via Ultralytics.
- Works best with a well-lit, front-facing webcam setup.
- Thresholds (`SLEEP_THRESHOLD_FRAMES`, `COVER_THRESHOLD_FRAMES`, eye-ratio cutoff) can be tuned based on your webcam's FPS.

## 👤 Author

**Prince Kumar** — Python Developer

---
If you found this project interesting, consider ⭐ starring the repo!
