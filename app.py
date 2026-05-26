import os
# 시스템 라이브러리 참조 경로를 현재 환경으로 강제 고정
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

import streamlit as st
import numpy as np

# OpenCV 로드를 안전하게 처리
try:
    import cv2
    st.write("OpenCV 로드 완료!")
except ImportError:
    st.error("시스템 환경 문제로 OpenCV를 로드할 수 없습니다.")

import mediapipe as mp
