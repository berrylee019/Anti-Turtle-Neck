import streamlit as st
import os
import cv2
import mediapipe as mp
import numpy as np

# 1. 환경 변수 강제 설정
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

st.title("🐢 거북목 방지 AI 시스템")

# 2. 실행 버튼 로직
if st.button("자세 분석 시작"):
    with st.spinner("AI 엔진을 로드 중입니다..."):
        try:
            # 엔진 로드
            mp_pose = mp.solutions.pose
            pose = mp_pose.Pose()
            mp_drawing = mp.solutions.drawing_utils
            
            st.success("AI 엔진 로드 성공!")
            
            # 카메라 캡처 및 분석 시작
            FRAME_WINDOW = st.image([])
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("카메라를 찾을 수 없습니다. 로컬 환경에서 테스트 중이신가요?")
            else:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret: break

                    # 3. 랜드마크 추출
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = pose.process(frame_rgb)

                    if results.pose_landmarks:
                        # 귀와 어깨 좌표 추출
                        landmarks = results.pose_landmarks.landmark
                        ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
                        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                        
                        # 4. 목 기울기 각도 계산
                        angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
                        
                        # 거북목 경고
                        if angle > 45: 
                            st.toast("🚨 거북목 주의! 허리를 펴주세요!", icon="🐢")
                        
                        # 랜드마크 그리기
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

                    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
                cap.release()

        except ImportError as e:
            st.error(f"라이브러리 로드 실패: {e}")
        except Exception as e:
            st.error(f"실행 중 오류 발생: {e}")
