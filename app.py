import sys
import os

# 시스템 환경 설정 (최소화)
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st
import cv2
import mediapipe as mp
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🐢 거북목 방지 AI 시스템")

# [중요] 세션 상태에 카메라 세션 보존
if 'camera_enabled' not in st.session_state:
    st.session_state.camera_enabled = False

# 1. 모델은 1번만 로드
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

# 2. 영상 처리 클래스
class PostureTransformer(VideoTransformerBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# 3. [최후의 보루] 레이아웃 강제 고정
# 사이드바나 다른 위젯을 추가하지 않고, 오직 스트리머만 배치하여 리렌더링 최소화
webrtc_streamer(
    key="posture",
    video_transformer_factory=PostureTransformer,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True # 비동기 처리로 루프 충돌 방지
)

st.write("---")
st.caption("카메라가 보이지 않는다면 브라우저 주소창의 자물쇠 아이콘을 눌러 권한을 허용해주세요.")
