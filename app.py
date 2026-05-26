import os
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st
# 다른 라이브러리보다 먼저 cv2를 시도하여 경로를 확보합니다.
try:
    import cv2
except ImportError:
    pass

import mediapipe as mp
import numpy as np

st.title("🐢 거북목 방지 AI 시스템")
