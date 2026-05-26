import streamlit as st
import numpy as np
import os

# OpenCV가 GUI 라이브러리를 찾지 않게 강제 설정
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

# 여기서 에러가 나면 OpenCV 설치 문제인데, 
# 이제 4.8.0 버전이므로 해결될 겁니다.
import cv2 
import mediapipe as mp

st.title("거북목 방지 AI 시작")
# 이제 여기에 형님의 기존 코드들을 하나씩 옮겨 담으시면 됩니다.
