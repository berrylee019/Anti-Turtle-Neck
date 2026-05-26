import sys
import os

os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st

st.title("🐢 거북목 방지 AI 시스템")

# 1. 세션 상태 초기화 (버튼을 눌렀는지 기억함)
if 'started' not in st.session_state:
    st.session_state.started = False

if st.button("자세 분석 시작") or st.session_state.started:
    st.session_state.started = True # 상태 유지
    with st.spinner("AI 엔진 로딩 중..."):
        try:
            import cv2
            import mediapipe as mp
            import numpy as np
            import av
            from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
            
            class PostureTransformer(VideoTransformerBase):
                def __init__(self):
                    self.mp_pose = mp.solutions.pose
                    self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
                    self.mp_drawing = mp.solutions.drawing_utils

                def recv(self, frame):
                    img = frame.to_ndarray(format="bgr24")
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = self.pose.process(img_rgb)
                    if results.pose_landmarks:
                        self.mp_drawing.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
                    return av.VideoFrame.from_ndarray(img, format="bgr24")

            webrtc_streamer(
                key="posture",
                video_transformer_factory=PostureTransformer,
                media_stream_constraints={"video": True, "audio": False}
            )
            
        except Exception as e:
            st.error(f"실행 오류: {e}")
