import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import streamlit.components.v1 as components

# 1. AI 엔진 로드
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(min_detection_confidencimport streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import streamlit.components.v1 as components

# 1. AI 엔진 로드 (고정)
@st.cache_resource
def get_pose_model():
    return mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

st.title("🐢 거북목 방지 AI 시스템")

# 2. 감지 모드 토글
run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    # 루프 대신 st.camera_input을 하나만 배치하고, 
    # 사진이 들어올 때마다 자동으로 처리를 수행하도록 구성합니다.
    img_file = st.camera_input("카메라를 켜주세요")
    
    if img_file:
        with st.spinner("AI가 분석 중..."):
            # 이미지 처리
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ear = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR]
                shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                
                angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
                
                # 결과 그리기
                mp_drawing.draw_landmarks(cv2_img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
                st.image(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))
                
                if angle > 45:
                    st.error("🚨 거북목 감지! 허리를 펴주세요!")
                    # 알림 호출
                    components.html("<script>new Notification('🐢 거북목 주의!');</script>", height=0)
                else:
                    st.success("✅ 바른 자세입니다.")
        
        # 3초 대기 후 자동으로 다음 스냅샷을 찍도록 유도
        time.sleep(3)
        st.rerun() 
else:
    st.write("감지 엔진이 중지되었습니다.")e=0.5, min_tracking_confidence=0.5)

pose = get_pose_model()
mp_drawing = mp.solutions.drawing_utils

st.title("🐢 거북목 방지 AI 시스템")

# 실시간 감지 토글
run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    # 2. 무한 루프 시작
    placeholder = st.empty() # 화면을 갱신하기 위한 공간
    
    while run_monitor:
        img_file = st.camera_input("분석 중...")
        
        if img_file:
            # 이미지 처리
            bytes_data = img_file.getvalue()
            cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
            img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
            results = pose.process(img_rgb)
            
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                ear = landmarks[mp.solutions.pose.PoseLandmark.LEFT_EAR]
                shoulder = landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
                
                angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
                
                if angle > 45:
                    st.error("🚨 거북목 감지! 허리를 펴주세요!")
                    # 알림 호출
                    components.html("<script>new Notification('🐢 거북목 주의!');</script>", height=0)
                else:
                    st.success("✅ 바른 자세 유지 중입니다.")
            
            time.sleep(2) # 2초마다 자동 재촬영
            st.rerun() # 화면을 다시 그려서 카메라를 다시 작동시킴
        
        run_monitor = st.toggle("감지 중지", value=True)
else:
    st.write("감지 엔진이 중지되었습니다.")
