import sys
import os

# [핵심] 시스템 그래픽 라이브러리 간섭 차단 및 렌더링 최적화
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.title("🐢 거북목 방지 AI 시스템")

# [핵심] AI 모델을 앱 실행 시 한 번만 로드하여 메모리에 고정 (루프 방지)
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5
    )

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

# 영상 처리 클래스 정의
class PostureTransformer(VideoTransformerBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # 랜드마크 추출
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img_rgb)
        
        # 랜드마크 그리기
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# [핵심] 버튼 없이 즉시 스트리머 배치 (세션 안정성 극대화)
st.info("카메라 장치를 선택하고 'Start'를 누르세요.")
webrtc_streamer(
    key="posture",
    video_transformer_factory=PostureTransformer,
    media_stream_constraints={"video": True, "audio": False}
)
