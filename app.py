import streamlit as st
from streamlit_webrtc import webrtc_streamer
import av
import mediapipe as mp
import cv2

st.title("🐢 거북목 방지 AI")

# 미디어파이프 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # 랜드마크 추출 및 그리기 로직 (앞서 만든 로직 적용)
    results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    if results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
    
    return av.VideoFrame.from_ndarray(img, format="bgr24")

webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
