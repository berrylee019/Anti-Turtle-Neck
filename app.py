import sys
import os
import streamlit as st

# OpenCV 빌드 오류 방지용 환경 변수
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

# 핵심: 시스템 경로를 강제로 비우고 라이브러리 참조를 단순화
st.set_page_config(page_title="거북목 AI")

st.title("🐢 거북목 방지 AI 시스템")

def start_posture_detection():
    # 1. 시스템 수준에서 경로를 한 번 더 체크
    try:
        import cv2
        import mediapipe as mp
        st.success("AI 엔진 로드 성공!")
    except ImportError as e:
        st.error(f"라이브러리 로드 실패: {e}")
        st.info("이 에러가 발생하면, 시스템 라이브러리 이슈입니다.")

if st.button("자세 분석 시작"):
    start_posture_detection()
