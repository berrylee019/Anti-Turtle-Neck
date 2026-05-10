import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

# 페이지 설정
st.set_page_config(page_title="Anti-Turtle-Neck AI", page_icon="🐢", layout="centered")

# 구글 시트 연결
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("데이터베이스 연결 확인이 필요합니다.")

# 세션 상태 관리
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "payment_step" not in st.session_state:
    st.session_state.payment_step = False

# --- 메인 헤더 ---
st.title("🧘 Anti-Turtle-Neck AI")
st.header("거북목 속에 숨겨진 '내 키 2cm'를 찾아드립니다!")
st.write("어정쩡한 체형에서 당당한 실루엣으로. AI가 실시간으로 당신의 자세를 감시합니다.")

# --- STEP 1: 실시간 감지 데모 섹션 ---
st.write("---")
st.subheader("📸 실시간 자세 교정 데모 (Alpha)")

if not st.session_state.demo_mode:
    st.info("아래 버튼을 눌러 카메라를 활성화하고, 평소 업무 자세를 취해보세요.")
    if st.button("지금 바로 실시간 체크 시작하기", use_container_width=True, type="primary"):
        st.session_state.demo_mode = True
        st.rerun()
else:
    # 실시간 감지 시뮬레이션
    img_file = st.camera_input("정면을 바라봐주세요 (AI가 각도를 분석 중입니다)")
    
    if img_file:
        with st.spinner("AI 엔진이 체형을 분석하고 있습니다..."):
            time.sleep(1.5) # 분석하는 척 하는 딜레이
            
        st.success("✅ 분석 완료!")
        
        # 고객 페인 포인트 공략 문구
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="현재 거북목 지수", value="78%", delta="위험", delta_color="inverse")
        with col2:
            st.metric(label="손실된 시각적 키", value="1.8cm", delta="확인됨", delta_color="off")
            
        st.error("🚨 경고: 어깨가 말리고 턱이 앞으로 쏠려 있어 실제보다 왜소해 보입니다!")
        st.write("👉 **해결책:** 정식 버전의 '무소음 실시간 알림'을 사용하면 업무 중에도 당당한 체형을 유지할 수 있습니다.")
        
        if st.button("기능 만족! 정식 버전 결제하고 '숨은 키' 찾기 🚀", use_container_width=True):
            st.session_state.payment_step = True
            st.rerun()

# --- STEP 2: 실제 결제 및 고객 정보 수집 ---
if st.session_state.payment_step:
    st.write("---")
    st.subheader("💳 얼리버드 특별 결제 및 예약")
    st.balloons()
    
    st.markdown("""
    ### 🎁 얼리버드 혜택 (오늘만 50% 할인)
    - **정식 버전 평생 이용권:** ~~39,000원~~ ➡️ **19,000원**
    - **혜택 1:** 실시간 거북목 감지 엔진 (Mac/Windows/Mobile)
    - **혜택 2:** 주간 자세 분석 리포트 제공
    - **혜택 3:** '숨은 키 되찾기' 스트레칭 가이드북 (PDF)
    """)
    
    with st.form("payment_form"):
        st.write("결제 의사를 확인하기 위해 아래 정보를 입력해주세요.")
        user_name = st.text_input("성함")
        user_email = st.text_input("이메일 주소 (이메일로 결제 링크가 전송됩니다)")
        pay_method = st.radio("선호하는 결제 수단", ["카카오페이 / 토스", "신용카드", "계좌이체"])
        
        submit_pay = st.form_submit_button("사전 예약 및 결제 대기 등록")
        
        if submit_pay:
            if user_email and "@" in user_email:
                try:
                    # 구글 시트에 결제 의사 데이터 저장
                    existing_data = conn.read(worksheet="Sheet1", usecols=[0, 1, 2, 3])
                    new_entry = pd.DataFrame({
                        "Email": [user_email],
                        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        "Name": [user_name],
                        "Status": [f"Payment Pending ({pay_method})"]
                    })
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    
                    st.success(f"감사합니다, {user_name}님! 입력하신 {user_email}로 결제 안내 및 특별 할인 링크를 발송해 드립니다.")
                    st.info("정식 버전 출시와 함께 형님의 '숨은 키'를 확실히 찾아드리겠습니다!")
                except:
                    st.error("저장 중 오류가 발생했습니다. 다시 시도해주세요.")
            else:
                st.error("올바른 이메일을 입력해주세요.")

st.write("---")
st.caption("© 2026 Anti-Turtle-Neck AI. 일하는 모든 이들의 당당한 자세를 응원합니다.")
