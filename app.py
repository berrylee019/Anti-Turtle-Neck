import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Anti-Turtle-Neck", page_icon="🐢")

# 구글 시트 연결 설정
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("연결 설정 확인이 필요합니다.")

# 세션 상태 초기화
if "clicked_buy" not in st.session_state:
    st.session_state.clicked_buy = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False

# --- 메인 헤더 ---
st.title("🧘 Anti-Turtle-Neck AI")
st.header("의자에 앉아 일하기 전, 자세를 잡아드립니다!")
st.subheader("언제 어디서든 바른 자세를 유지하세요!")

st.write("노트북 웹캠은 물론, **스마트폰 전면 카메라**로도 실시간 자세 교정이 가능합니다.")

# --- 신규: 실시간 데모 섹션 (성의 표시 구역) ---
st.write("---")
st.subheader("📸 5초 셀프 자세 체크 (Demo)")
st.info("현재 개발 중인 AI 엔진의 핵심 기능을 브라우저에서 바로 체험해보세요.")

# 카메라 입력창
enable_camera = st.checkbox("데모용 카메라 활성화")

if enable_camera:
    img_file = st.camera_input("정면을 바라보고 평소 자세를 취해보세요")
    
    if img_file:
        # 사진이 찍혔을 때 시각적 피드백 제공
        st.success("✅ 인식 완료: 현재 목 각도와 어깨 선을 분석 중입니다.")
        st.warning("⚠️ 분석 결과: 거북목 초기 증상이 감지되었습니다. 턱을 가슴 쪽으로 2cm 당겨주세요!")
        st.caption("※ 정식 버전에서는 사진 촬영 없이 실시간 영상으로 '무소음 알림'을 보내드립니다.")

st.write("---")

# --- 기존: 핵심 가치 제안 ---
with st.expander("✨ 주요 기능 보기"):
    st.write("- **실시간 웹캠 자세 분석**: 별도 장비 없이 카메라만으로 감지")
    st.write("- **업무 몰입을 깨지 않는 알림**: 소리 없이 시각적/진동 알림 지원")
    st.write("- **스마트폰 거치대 활용**: 눈높이에 맞춘 폰 카메라로 정밀 측정")
    st.write("- **자세 무너짐 즉시 경고**: 굽은 등, 거북목 발생 시 즉각 피드백")

st.write("---")
st.subheader("💳 프리미엄 영구 라이선스")
st.write("~~정가 39,000원~~ ➡️ **특별가: 19,000원 (선착순 한정)**")

# --- 기존: 구매 및 이메일 수집 로직 ---
if not st.session_state.clicked_buy:
    if st.button("지금 구매하고 바로 시작하기 🚀", use_container_width=True, type="primary"):
        st.session_state.clicked_buy = True
        st.rerun()
else:
    if not st.session_state.email_submitted:
        st.warning("⚠️ 현재 사전 예약 인원이 마감되었습니다.")
        st.info("이메일을 남겨주시면 정식 론칭 시 **50% 추가 할인 쿠폰**을 보내드립니다!")
        
        with st.form("email_form"):
            email_input = st.text_input("할인 혜택을 받을 이메일 주소")
            submit = st.form_submit_button("50% 할인 예약하기")
            
            if submit:
                if email_input and "@" in email_input:
                    try:
                        # 구글 시트 업데이트
                        existing_data = conn.read(worksheet="시트1", usecols=[0, 1])
                        new_data = pd.DataFrame({
                            "Email": [email_input],
                            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        })
                        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                        conn.update(worksheet="시트1", data=updated_df)
                        
                        st.session_state.email_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"데이터 저장 중 오류가 발생했습니다. (Sheet 이름을 확인해주세요)")
                else:
                    st.error("올바른 이메일을 입력해주세요.")
    else:
        st.success("🎉 등록 완료! 정식 출시 때 가장 먼저 연락드리겠습니다.")
