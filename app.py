import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time
import streamlit.components.v1 as components

# --- 1. 페이지 설정 및 스타일링 ---
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

# --- 2. 자바스크립트: 무소음 알림 엔진 ---
# 이 JS 코드는 브라우저 시스템 알림을 제어합니다.
js_engine = """
<script>
function askPermission() {
    Notification.requestPermission();
}
function sendSilentNotification(title, body) {
    if (Notification.permission === "granted") {
        new Notification(title, {
            body: body,
            silent: true  // 무소음 핵심 설정
        });
    }
}
</script>
"""
components.html(js_engine, height=0)

# --- 3. 로그인 시스템 ---
def login():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-card">', unsafe_allow_html=True)
            st.image("https://cdn-icons-png.flaticon.com/512/3022/3022221.png", width=80)
            st.title("Anti-Turtle-Neck AI")
            st.write("서비스 이용을 위해 비밀번호를 입력해주세요.")
            password = st.text_input("Password", type="password", placeholder="Enter secret password")
            
            if st.button("Login", use_container_width=True):
                if password == st.secrets["LOGIN_PASSWORD"]:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("비밀번호가 일치하지 않습니다.")
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

login()

# --- 4. 메인 앱 로직 시작 ---
# 구글 시트 연결
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
except Exception:
    st.error("연결 설정 확인이 필요합니다.")

# 세션 상태 초기화
if "clicked_buy" not in st.session_state:
    st.session_state.clicked_buy = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False
if "monitoring_active" not in st.session_state:
    st.session_state.monitoring_active = False

# 헤더 영역
st.success("🔓 로그인 성공! 프리미엄 모니터링 모드 활성화")
st.title("🧘 Anti-Turtle-Neck AI")
st.header("거북목 속에 숨겨진 '내 키 2cm'를 찾아드립니다!")

# --- 5. 실시간 무소음 알림 데모 섹션 ---
st.write("---")
st.subheader("📸 실시간 무소음 감지 모드")
st.info("업무 중에 자세가 무너지면 시스템 알림이 '조용히' 찾아옵니다.")

# 알림 권한 요청 버튼
if st.button("🔔 실시간 알림 권한 허용하기"):
    components.html("<script>Notification.requestPermission();</script>", height=0)
    st.toast("상단 브라우저 팝업에서 '허용'을 눌러주세요!")

# 모니터링 토글
run_monitor = st.toggle("실시간 AI 감지 엔진 가동")

if run_monitor:
    st.session_state.monitoring_active = True
    img_file = st.camera_input("카메라가 당신의 자세를 실시간 분석 중입니다", label_visibility="collapsed")
    
    if img_file:
        with st.spinner("AI가 체형 각도를 계산 중..."):
            time.sleep(2) # 분석 시뮬레이션
        
        # 실제 알림 발송 (JS 호출)
        alert_script = """
        <script>
        if (Notification.permission === "granted") {
            new Notification("🚨 Anti-Turtle-Neck 감지", {
                body: "지금 목이 앞으로 쏠렸습니다! 어깨를 펴고 숨은 키 2cm를 되찾으세요.",
                silent: true
            });
        }
        </script>
        """
        components.html(alert_script, height=0)
        
        st.error("🚨 거북목 감지! 조용히 전송된 시스템 알림을 확인하고 자세를 바로잡으세요.")
        st.metric(label="손실된 시각적 키", value="1.8cm", delta="즉시 교정 필요", delta_color="inverse")
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
                        st.error("데이터 저장 오류. 구글 시트에 Name, Note 열이 있는지 확인해주세요.")
                else:
                    st.error("올바른 이메일을 입력해주세요.")
    else:
        st.success("🎉 등록 완료! 입력하신 이메일로 곧 특별 결제 링크를 보내드리겠습니다.")

st.write("---")
st.caption("© 2026 Anti-Turtle-Neck AI. 모든 메이커의 당당한 자세를 응원합니다.")
