import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from ultralytics import YOLO

st.set_page_config(page_title="AI Study Monitor", page_icon="🎓", layout="centered")

st.title("🎓 AI Study Monitor — Live Demo")
st.write(
    "This AI watches you through your webcam and warns you in real time if it "
    "detects you **sleeping**, **using your phone**, or **hiding your face**. "
    "Click **Start** below and allow camera access."
)

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Load models once and cache across reruns
@st.cache_resource
def load_models():
    face_detector = FaceMeshDetector(maxFaces=1)
    phone_detector = YOLO("yolov8n.pt")
    return face_detector, phone_detector

face_detector, phone_detector = load_models()
classNames = phone_detector.names

# Landmark indices for sleep detection
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
FACE_LEFT = 130
FACE_RIGHT = 243

SLEEP_THRESHOLD_FRAMES = 15
COVER_THRESHOLD_FRAMES = 20


class StudyMonitorProcessor(VideoProcessorBase):
    def __init__(self):
        self.closed_frames = 0
        self.covered_frames = 0

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # ---------- Sleep & face-cover detection ----------
        img, faces = face_detector.findFaceMesh(img, draw=False)
        is_sleepy = False
        is_face_covered = False

        if faces:
            self.covered_frames = 0
            face = faces[0]
            eye_dist, _ = face_detector.findDistance(face[LEFT_EYE_TOP], face[LEFT_EYE_BOTTOM])
            face_dist, _ = face_detector.findDistance(face[FACE_LEFT], face[FACE_RIGHT])
            ratio = (eye_dist / face_dist) * 100

            if ratio < 11.0:
                self.closed_frames += 1
            else:
                self.closed_frames = 0

            if self.closed_frames >= SLEEP_THRESHOLD_FRAMES:
                is_sleepy = True

            cvzone.putTextRect(img, f"Eye Ratio: {int(ratio)}", (30, 40), scale=1, thickness=1)
        else:
            self.closed_frames = 0
            self.covered_frames += 1
            if self.covered_frames >= COVER_THRESHOLD_FRAMES:
                is_face_covered = True

        # ---------- Phone detection ----------
        results = phone_detector.predict(img, stream=True, verbose=False)
        phone_detected = False
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if classNames[cls_id] == "cell phone" and conf > 0.5:
                    phone_detected = True
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
                    cvzone.putTextRect(
                        img, f"Phone detected! {int(conf * 100)}%",
                        (x1, max(y1 - 10, 30)), scale=1, thickness=1, colorR=(255, 0, 255)
                    )

        # ---------- On-screen warning (priority order) ----------
        if is_face_covered:
            cvzone.putTextRect(img, "DONT COVER YOUR FACE!", (50, 100), scale=2, thickness=3, colorR=(0, 0, 255))
        elif is_sleepy:
            cvzone.putTextRect(img, "WAKE UP & STUDY!", (50, 100), scale=2, thickness=3, colorR=(0, 0, 255))
        elif phone_detected:
            cvzone.putTextRect(img, "PUT THE PHONE AWAY!", (50, 100), scale=2, thickness=3, colorR=(0, 165, 255))

        return av.VideoFrame.from_ndarray(img, format="bgr24")


webrtc_streamer(
    key="study-monitor",
    video_processor_factory=StudyMonitorProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
)

st.caption(
    "⚠️ Runs entirely in your browser session — no video is stored or sent anywhere. "
    "Audio alerts are disabled in this web version; watch for the on-screen warning text instead."
)
