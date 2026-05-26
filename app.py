import streamlit as st
import os
import cv2
import mediapipe as mp
import numpy as np
import av
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# 1. 환경 변수 강제 설정
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

st.title("🐢 거북목 방지 AI 시스템")

# 2. 영상 처리 클래스 정의
class PostureTransformer(VideoTransformerBase):
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.mp_drawing = mp.solutions.drawing_utils

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        
        # 랜드마크 추출 및 처리
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            ear = landmarks[self.mp_pose.PoseLandmark.LEFT_EAR]
            shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            
            # 각도 계산
            angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
            
            # 거북목 경고 (토스트는 메인 스레드에서 호출해야 하므로 여기서는 각도 정보만 활용)
            if angle > 45:
                pass # 알림은 UI 스레드와 별개로 처리해야 함
            
            # 랜드마크 그리기
            self.mp_drawing.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# 3. 메인 로직
if st.button("자세 분석 시작"):
    with st.spinner("AI 엔진을 로드 중입니다..."):
        try:
            st.success("AI 엔진 로드 성공!")
            # webrtc_streamer 호출
            webrtc_streamer(
                key="posture-analysis",
                video_transformer_factory=PostureTransformer,
                media_stream_constraints={"video": True, "audio": False}
            )
        except Exception as e:
            st.error(f"실행 중 오류 발생: {e}")
