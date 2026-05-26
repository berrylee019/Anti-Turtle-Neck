import sys
import os
os.environ["OPENCV_VIDEOIO_PRIORITY_BACKEND"] = "FFMPEG"
sys.setdlopenflags(os.RTLD_GLOBAL | os.RTLD_LAZY)
import numpy as np
import cv2
import mediapipe as mp
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import streamlit.components.v1 as components
# from streamlit_gsheets import GSheetsConnection  <-- 일단 주석 처리


# --- 1. 세션 상태 초기화 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "clicked_buy" not in st.session_state:
    st.session_state.clicked_buy = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False
if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False

# MediaPipe Pose 설정
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

# --- 2. 페이지 설정 ---
st.set_page_config(page_title="Anti-Turtle-Neck", page_icon="🐢", layout="centered")

# --- 4. 메인 앱 로직 ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("연결 설정 확인이 필요합니다.")

col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.image("turtle-neck.png", use_container_width=True, caption="Anti-Turtle-Neck AI가 당신의 당당한 자세를 응원합니다.")

st.title("🧘 Anti-Turtle-Neck AI")
st.header("거북목 속에 숨겨진 '내 키 2cm'를 찾아드립니다!")

# --- 5. 실시간 무소음 감지 모드 (MediaPipe 연동) ---
st.write("---")
st.subheader("📸 실시간 무소음 감지 모드")
st.info("AI 모델이 실시간으로 귀와 어깨의 각도를 정밀 분석합니다.")

if st.button("🔔 실시간 알림 권한 허용하기"):
    components.html("<script>Notification.requestPermission();</script>", height=0)
    st.toast("상단 브라우저 팝업에서 '허용'을 눌러주세요!")

run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    st.session_state.monitoring_active = True
    img_file = st.camera_input("카메라 분석 중...", label_visibility="collapsed")
    
    if img_file:
        with st.spinner("이미지 프레임 처리 중..."):
            # 이미지 데이터 변환
            image = np.array(bytearray(img_file.read()), dtype=np.uint8)
            img = cv2.imdecode(image, 1)
            
            # MediaPipe 분석
            results = pose.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            
            if results.pose_landmarks:
                # 7: 귀, 11: 어깨 좌표
                ear = results.pose_landmarks.landmark[7]
                shoulder = results.pose_landmarks.landmark[11]
                
                # 라디안을 각도로 변환
                angle = abs(np.degrees(np.arctan2(shoulder.y - ear.y, shoulder.x - ear.x)))
                
                st.write("🔍 특징점(Landmarks) 추출 완료")
                
                st.markdown("### 분석 리포트")
                col1, col2 = st.columns(2)
                col1.metric("경추 각도", f"{angle:.1f}°")
                col2.metric("분석 상태", "정상" if angle < 45 else "교정 필요")
                
                # 임계값(45도) 기준으로 거북목 판정
                if angle > 45:
                    components.html("""
                    <script>
                        if (Notification.permission === "granted") {
                            new Notification("🚨 Anti-Turtle-Neck 감지", {
                                body: "지금 목이 앞으로 나왔습니다! 어깨를 펴세요.",
                                silent: true
                            });
                        }
                    </script>
                    """, height=0)
                    st.error("🚨 경고: 거북목이 감지되었습니다.")
                    st.warning("💡 턱을 안으로 당겨 자세를 교정하세요!")
                else:
                    st.success("✅ 완벽한 자세입니다! 지금처럼 유지하세요.")
            else:
                st.warning("⚠️ 신체가 인식되지 않았습니다. 정면을 바라보고 다시 촬영해주세요.")

st.write("---")

# --- 6. 정식 버전 안내 (이하 기존 코드 유지) ---
with st.expander("✨ 정식 버전 출시 혜택 보기"):
    st.write("- **실시간 무소음 알림**: 소리 없이 시각적 피드백으로 집중력 유지")
    st.write("- **정밀 체형 분석**: 단순 각도를 넘어 어깨 말림(Round Shoulder)까지 감지")
    st.write("- **주간 자세 리포트**: 한 주간 내 자세가 얼마나 좋아졌는지 데이터로 확인")

# ... (결제 로직 및 푸터 등 기존 코드 유지) ...
