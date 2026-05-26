import cv2
import mediapipe as mp
import numpy as np
import streamlit as st

# 1. 미디어파이프 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# 2. 실시간 카메라 캡처를 위한 빈 공간 생성
FRAME_WINDOW = st.image([])
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    # 3. 랜드마크 추출
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(frame_rgb)

    if results.pose_landmarks:
        # 귀(landmark 7)와 어깨(landmark 11) 좌표 추출
        landmarks = results.pose_landmarks.landmark
        ear = landmarks[mp_pose.PoseLandmark.LEFT_EAR]
        shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        
        # 4. 각도 계산 (y좌표 차이를 이용한 목 기울기)
        angle = np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x))
        
        # 거북목 경고 로직 (예: 각도가 특정 값 이상일 때)
        if angle > 45: # 임계값은 테스트하며 조절하세요
            st.toast("🚨 거북목 주의! 허리를 펴주세요!", icon="🐢")
        
        # 랜드마크 그리기
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    FRAME_WINDOW.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

cap.release()
