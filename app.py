import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import streamlit.components.v1 as components

# 1. AI 모델 캐싱 (앱 전체에서 1번만 로드)
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

st.title("🐢 거북목 방지 AI 시스템")

# 2. 감지 모드 토글
run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    # 3. 카메라 입력 (루프 에러 방지를 위해 하나만 배치)
    img_file = st.camera_input("카메라를 켜주세요")
    
    if img_file:
        with st.spinner("AI가 분석 중..."):
            # 이미지 변환
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ear = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR]
                shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                
                # 각도 계산
                angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
                
                # 랜드마크 표시
                mp_drawing.draw_landmarks(cv2_img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
                
                if angle > 45:
                    st.error("🚨 거북목 감지! 허리를 펴주세요!")
                    # 알림 호출
                    components.html("<script>new Notification('🐢 거북목 주의!');</script>", height=0)
                else:
                    st.success("✅ 바른 자세입니다.")
        
        # 3초 후 자동으로 화면 갱신 (연속 촬영 효과)
        time.sleep(3)
        st.rerun() 
else:
    st.write("감지 엔진이 중지되었습니다. 토글을 켜서 시작하세요.")
