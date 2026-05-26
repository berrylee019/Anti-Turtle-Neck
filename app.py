import sys
import os

# [핵심] 시스템 라이브러리 간섭 차단 및 오프스크린 렌더링 강제 설정
os.environ["QT_QPA_PLATFORM"] = "offscreen"
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st

st.title("🐢 거북목 방지 AI 시스템")

if st.button("자세 분석 시작"):
    with st.spinner("AI 엔진을 로드 중입니다..."):
        try:
            # 의존성 로드
            import cv2
            import mediapipe as mp
            import numpy as np
            import av
            from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
            
            st.success("AI 엔진 로드 성공!")

            class PostureTransformer(VideoTransformerBase):
                def __init__(self):
                    self.mp_pose = mp.solutions.pose
                    # 시스템 OpenGL 의존성을 줄이기 위해 간단한 모델 사용
                    self.pose = self.mp_pose.Pose(
                        static_image_mode=False,
                        min_detection_confidence=0.5,
                        min_tracking_confidence=0.5
                    )
                    self.mp_drawing = mp.solutions.drawing_utils

                def recv(self, frame):
                    img = frame.to_ndarray(format="bgr24")
                    
                    # 렌더링 방식 우회: 색상 변환 후 처리
                    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = self.pose.process(img_rgb)

                    if results.pose_landmarks:
                        self.mp_drawing.draw_landmarks(
                            img, 
                            results.pose_landmarks, 
                            self.mp_pose.POSE_CONNECTIONS
                        )
                    return av.VideoFrame.from_ndarray(img, format="bgr24")

            webrtc_streamer(
                key="posture",
                video_transformer_factory=PostureTransformer,
                media_stream_constraints={"video": True, "audio": False}
            )
            
        except ImportError as e:
            st.error(f"라이브러리 로드 실패: {e}")
            st.info("requirements.txt를 다시 확인해주세요.")
        except Exception as e:
            st.error(f"실행 중 오류 발생: {e}")
