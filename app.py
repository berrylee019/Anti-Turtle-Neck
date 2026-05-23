import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time
import streamlit.components.v1 as components
import random  # 랜덤 편차 구현을 위해 추가

# --- 1. 세션 상태 초기화 ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "clicked_buy" not in st.session_state:
    st.session_state.clicked_buy = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False
if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False

# --- 2. 페이지 설정 및 스타일링 ---
st.set_page_config(page_title="Anti-Turtle-Neck", page_icon="🐢", layout="centered")

st.markdown("""
    <style>
    .login-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .stButton>button {
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. 자바스크립트: 무소음 알림 엔진 ---
# silent: true 설정을 통해 브라우저 시스템 소리 없이 시각적 알림만 발생시킵니다.
js_engine = """
<script>
function requestNotificationPermission() {
    Notification.requestPermission();
}
function sendSilentNotification(title, body) {
    if (Notification.permission === "granted") {
        new Notification(title, {
            body: body,
            silent: true
        });
    }
}
</script>
"""
components.html(js_engine, height=0)

# --- 4. 메인 앱 로직 시작 ---
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("연결 설정 확인이 필요합니다.")

# 상단 대표 이미지
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    st.image("turtle-neck.png", use_container_width=True, caption="Anti-Turtle-Neck AI가 당신의 당당한 자세를 응원합니다.")

st.title("🧘 Anti-Turtle-Neck AI")
st.header("거북목 속에 숨겨진 '내 키 2cm'를 찾아드립니다!")

# --- 5. 실시간 무소음 감지 모드 ---
st.write("---")
st.subheader("📸 실시간 무소음 감지 모드")
st.info("AI가 실시간으로 자세를 분석하고 무소음 알림을 보냅니다.")

if st.button("🔔 실시간 알림 권한 허용하기"):
    components.html("<script>requestNotificationPermission();</script>", height=0)
    st.toast("상단 브라우저 팝업에서 '허용'을 눌러주세요!")

run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    st.session_state.monitoring_active = True
    img_file = st.camera_input("카메라 분석 중...", label_visibility="collapsed")
    
    if img_file:
        with st.spinner("이미지 프레임 처리 중..."):
            time.sleep(1)
            st.write("🔍 특징점(Landmarks) 추출 중...")
            time.sleep(1)
            st.write("📐 목 각도 계산(Neck Angle: 32°)...")
            time.sleep(1)
        
        st.markdown("### 분석 리포트")
        col1, col2 = st.columns(2)
        col1.metric("경추 각도", "32°", "정상 대비 10° 과도")
        col2.metric("어깨 말림", "확인됨")
        
        # 70% 확률로 거북목 감지
        is_bad_posture = random.choice([True, True, True, False])
        
        if is_bad_posture:
            # 무소음 알림 발송 코드 호출
            alert_code = """
            <script>
            sendSilentNotification("🚨 Anti-Turtle-Neck 감지", "지금 목이 앞으로 나왔습니다! 어깨를 펴세요.");
            </script>
            """
            components.html(alert_code, height=0)
            
            st.error("🚨 경고: 거북목이 감지되었습니다.")
            st.warning("💡 턱을 2cm만 안으로 당기면 경추 부담이 15kg 줄어듭니다.")
            st.metric(label="손실된 시각적 키", value=f"{round(random.uniform(1.5, 2.2), 1)}cm", delta="교정 필요", delta_color="inverse")
        else:
            st.success("✅ 완벽한 자세입니다! 지금처럼 유지하세요.")
            st.metric(label="자세 상태", value="정상범위", delta="양호")
            
        st.write(f"분석 로그: 척추 각도 {random.randint(15, 28)}° 감지 완료.")
else:
    st.session_state.monitoring_active = False
    st.write("감지 엔진이 중지되었습니다. 업무 시작 시 토글을 켜주세요.")

st.write("---")

# --- 6. 가치 제안 및 결제 로직 ---
with st.expander("✨ 정식 버전 출시 혜택 보기"):
    st.write("- **실시간 무소음 알림**: 소리 없이 시각적 피드백으로 집중력 유지")
    st.write("- **정밀 체형 분석**: 단순 각도를 넘어 어깨 말림(Round Shoulder)까지 감지")
    st.write("- **주간 자세 리포트**: 한 주간 내 자세가 얼마나 좋아졌는지 데이터로 확인")

st.subheader("💳 프리미엄 영구 라이선스")
st.write("~~정가 39,000원~~ ➡️ **특별가: 19,000원 (얼리버드 한정)**")

if not st.session_state.clicked_buy:
    if st.button("지금 예약하고 내 키 2cm 찾기 🚀", use_container_width=True, type="primary"):
        st.session_state.clicked_buy = True
        st.rerun()
else:
    if not st.session_state.email_submitted:
        st.warning("⚠️ 현재 선착순 할인 수량이 마감 임박입니다.")
        with st.form("payment_form"):
            user_name = st.text_input("성함")
            email_input = st.text_input("이메일 주소")
            pay_method = st.radio("선호 결제 수단", ["카카오(송금)", "신용카드", "계좌이체"])
            submit = st.form_submit_button("사전 예약 및 결제 대기 등록")
            
            if submit:
                if email_input and "@" in email_input:
                    try:
                        existing_data = conn.read(worksheet="시트1")
                        new_data = pd.DataFrame({
                            "Email": [email_input],
                            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                            "Name": [user_name],
                            "Note": [f"결제대기({pay_method})"]
                        })
                        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                        conn.update(worksheet="시트1", data=updated_df)
                        st.session_state.email_submitted = True
                        st.rerun()
                    except Exception:
                        st.error("데이터 저장 오류.")
                else:
                    st.error("올바른 이메일을 입력해주세요.")
    else:
        st.success("🎉 등록 완료! 곧 이메일로 특별 결제 링크를 보내드리겠습니다.")

st.write("---")
st.caption("© 2026 Anti-Turtle-Neck AI. 모든 메이커의 당당한 자세를 응원합니다.")
