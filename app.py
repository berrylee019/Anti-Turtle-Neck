import streamlit as st
import os

# 1. 환경 변수 강제 설정 (시스템 라이브러리 간섭 차단)
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"

st.title("🐢 거북목 방지 AI 시스템")

# 2. 실행 버튼을 눌러야만 라이브러리를 로드 (가장 안전)
if st.button("자세 분석 시작"):
    with st.spinner("AI 엔진을 로드 중입니다..."):
        try:
            import cv2
            import mediapipe as mp
            st.success("AI 엔진 로드 성공!")
            # 이후 로직...
        except ImportError as e:
            st.error(f"라이브러리 로드 실패: {e}")
            st.warning("서버 환경이 최신(Python 3.14)이라 호환성 문제가 발생하고 있습니다.")
