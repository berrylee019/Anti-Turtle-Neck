import sys
import os

# [핵심] 바이너리 충돌 방지를 위한 시스템 패치
sys.setrecursionlimit(2000)
os.environ["PYTHONPATH"] = "/home/adminuser/venv/lib/python3.14/site-packages"

# 1. 환경 변수 강제 설정
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st

st.title("🐢 거북목 방지 AI 시스템")

# 3. 메인 로직
if st.button("자세 분석 시작"):
    with st.spinner("AI 엔진을 로드 중입니다..."):
        try:
            # [핵심] 라이브러리 임포트 위치를 버튼 안으로 이동
            import cv2
            import mediapipe as mp
            import numpy as np
            import av
            from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
            
            st.success("AI 엔진 로드 성공!")

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
                        
                        # 랜드마크 그리기
                        self.mp_drawing.draw_landmarks(img, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)

                    return av.VideoFrame.from_ndarray(img, format="bgr24")

            # webrtc_streamer 호출
            webrtc_streamer(
                key="posture-analysis",
                video_transformer_factory=PostureTransformer,
                media_stream_constraints={"video": True, "audio": False}
            )
            
        except ImportError as e:
            st.error(f"라이브러리 로드 실패 (의존성 확인 필요): {e}")
        except Exception as e:
            st.error(f"실행 중 오류 발생: {e}")
