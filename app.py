import streamlit as st
import numpy as np
import os

# OpenCV가 설치된 환경과 관계없이 FFMPEG 백엔드를 사용하도록 강제
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

# 메인 기능 함수 내부에서 import 하도록 설계
def get_cv2():
    import cv2
    return cv2

def get_mediapipe():
    import mediapipe as mp
    return mp

st.title("거북목 방지 AI 시스템")

# 이후 코드에서 cv2나 mediapipe가 필요할 때마다 호출
# 예: cap = get_cv2().VideoCapture(0)
