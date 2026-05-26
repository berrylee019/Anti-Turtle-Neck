import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import streamlit.components.v1 as components

# 1. AI 엔진 로드 (세션에 고정)
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

st.title("🐢 거북목 방지 AI 시스템")

# 2. 실시간 감지 모드
run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    # st.camera_input을 사용하여 찰칵! 찍어서 분석하는 방식 (매우 안정적)
    img_file = st.camera_input("분석할 자세를 촬영하세요")
    
    if img_file:
        with st.spinner("AI가 체형 각도를 계산 중..."):
            # 바이트 데이터를 OpenCV 이미지로 변환
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            
            # 분석 로직
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ear = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR]
                shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                
                # 각도 계산
                angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
                
                # 결과 시각화
                mp_drawing.draw_landmarks(cv2_img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
                
                if angle > 45:
                    st.error("🚨 거북목 감지! 허리를 펴주세요!")
                    # 알림 스크립트 실행
                    alert_script = """
                    <script>
                        if (Notification.permission === "granted") {
                            new Notification("🚨 Anti-Turtle-Neck 감지", {
                                body: "지금 목이 앞으로 쏠렸습니다! 어깨를 펴세요.",
                                silent: true
                            });
                        }
                    </script>
                    """
                    components.html(alert_script, height=0)
                else:
                    st.success("✅ 바른 자세입니다!")
else:
    st.write("감지 엔진이 중지되었습니다. 토글을 켜서 시작하세요.")
