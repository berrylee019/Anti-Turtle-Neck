import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import time

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
if "demo_analyzed" not in st.session_state:
    st.session_state.demo_analyzed = False

# --- 메인 헤더 ---
st.title("🧘 Anti-Turtle-Neck AI")
st.header("거북목 속에 숨겨진 '내 키 2cm'를 찾아드립니다!")
st.subheader("어정쩡한 체형에서 당당한 실루엣으로, AI가 실시간으로 감시합니다.")

# --- 신규: 실시간 데모 및 분석 섹션 ---
st.write("---")
st.subheader("📸 5초 실시간 자세 분석 (Demo)")
st.info("카메라를 활성화하여 현재 본인의 거북목 상태와 '손실된 키'를 확인해보세요.")

enable_camera = st.checkbox("데모용 카메라 활성화")

if enable_camera:
    img_file = st.camera_input("정면을 바라보고 평소 업무 자세를 취해보세요")
    
    if img_file:
        with st.spinner("AI 엔진이 체형을 분석 중입니다..."):
            time.sleep(1.5) # 분석 시뮬레이션
        
        st.success("✅ 분석 완료!")
        
        # 고객 페인 포인트 맞춤형 피드백
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="현재 거북목 지수", value="78%", delta="위험", delta_color="inverse")
        with col2:
            st.metric(label="손실된 시각적 키", value="1.8cm", delta="감지됨", delta_color="off")
            
        st.warning("🚨 분석 결과: 어깨가 안으로 말리고 턱이 돌출되어 실제보다 왜소해 보입니다.")
        st.info("💡 정식 버전의 '무소음 실시간 알림'을 사용하면 업무 중에도 이 키를 유지할 수 있습니다.")
        st.session_state.demo_analyzed = True

st.write("---")

# --- 기존: 핵심 가치 제안 ---
with st.expander("✨ 정식 버전 주요 기능 보기"):
    st.write("- **실시간 웹캠 자세 분석**: 별도 장비 없이 카메라만으로 감지")
    st.write("- **업무 몰입을 깨지 않는 알림**: 소리 없이 시각적/진동 알림 지원")
    st.write("- **숨은 키 되찾기**: 당당한 체형 유지를 위한 실시간 피드백")
    st.write("- **스마트폰 거치대 활용**: 눈높이에 맞춘 폰 카메라로 정밀 측정")

st.write("---")
st.subheader("💳 프리미엄 영구 라이선스")
st.write("~~정가 39,000원~~ ➡️ **특별가: 19,000원 (얼리버드 한정)**")

# --- 수정된 결제 및 데이터 저장 로직 ---
if not st.session_state.clicked_buy:
    if st.button("지금 예약하고 숨은 키 찾기 🚀", use_container_width=True, type="primary"):
        st.session_state.clicked_buy = True
        st.rerun()
else:
    if not st.session_state.email_submitted:
        st.warning("⚠️ 현재 사전 예약 인원이 마감 임박입니다.")
        st.info("정보를 남겨주시면 정식 론칭 시 **결제 안내 및 50% 할인 링크**를 보내드립니다.")
        
        with st.form("payment_form"):
            user_name = st.text_input("성함")
            email_input = st.text_input("이메일 주소")
            pay_method = st.radio("선호 결제 수단", ["카카오/토스", "신용카드", "계좌이체"])
            submit = st.form_submit_button("사전 예약 및 결제 대기 등록")
            
            if submit:
                if email_input and "@" in email_input:
                    try:
                        # 구글 시트 데이터 읽기
                        # 에러 방지를 위해 열 개수를 제한하지 않고 읽어옴
                        existing_data = conn.read(worksheet="시트1")
                        
                        # 새 데이터 생성 (형님의 시트 구조에 맞게 컬럼명 매칭)
                        new_data = pd.DataFrame({
                            "Email": [email_input],
                            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                            "Name": [user_name],
                            "Note": [f"결제대기({pay_method})"]
                        })
                        
                        # 기존 데이터와 합치기 (새 컬럼이 생겨도 유연하게 대응)
                        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                        
                        # 구글 시트 업데이트
                        conn.update(worksheet="시트1", data=updated_df)
                        
                        st.session_state.email_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"데이터 저장 중 오류가 발생했습니다. 구글 시트에 'Name'과 'Note' 열을 추가해주세요.")
                else:
                    st.error("올바른 이메일을 입력해주세요.")
    else:
        st.success("🎉 예약 완료! 입력하신 이메일로 곧 특별 결제 링크를 보내드리겠습니다.")

st.write("---")
st.caption("© 2026 Anti-Turtle-Neck AI. 모든 메이커의 당당한 자세를 응원합니다.")
