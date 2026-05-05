import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Anti-Turtle-Neck", page_icon="🐢")

# 구글 시트 연결 설정
conn = st.connection("gsheets", type=GSheetsConnection)

# 세션 상태 초기화
if "clicked_buy" not in st.session_state:
    st.session_state.clicked_buy = False
if "email_submitted" not in st.session_state:
    st.session_state.email_submitted = False

# 헤드카피
st.title("🧘 AI 자세 교정 도우미")
st.header("의자에 앉아 일하기 전, 자세를 잡아드립니다!")
st.subheader("언제 어디서든 바른 자세를 유지하세요!")

st.write("노트북 웹캠은 물론, **스마트폰 전면 카메라**로도 실시간 자세 교정이 가능합니다. "
         "책상 위 거치대에 폰을 올려두고, 거북목으로부터 목 건강을 지키세요!")

# 핵심 가치 제안
with st.expander("✨ 주요 기능 보기"):
    st.write("- 실시간 웹캠 자세 분석")
    st.write("- 업무 몰입을 깨지 않는 무소음 알림")
    st.write("- 스마트폰을 눈높이 거치대에 올려둡니다.")
    st.write("- 전면 카메라가 얼굴을 정면으로 비추게 설정합니다.")
    st.write("- 자세가 무너지면 진동이나 화면 알림으로 즉시 알려드립니다.")

st.write("---")
st.subheader("💳 프리미엄 영구 라이선스")
st.write("~~정가 39,000원~~ ➡️ **특별가: 19,000원 (선착순 한정)**")

# 구매 및 이메일 수집 로직
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
                        # 1. 기존 데이터 읽기 (시트가 비어있을 경우 대비)
                        existing_data = conn.read(worksheet="시트1", usecols=[0, 1])
                        
                        # 2. 새 데이터 생성
                        new_data = pd.DataFrame({
                            "Email": [email_input],
                            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                        })
                        
                        # 3. 데이터 합치기 및 구글 시트 업데이트
                        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                        conn.update(worksheet="시트1", data=updated_df)
                        
                        st.session_state.email_submitted = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
                else:
                    st.error("올바른 이메일을 입력해주세요.")
    else:
        st.success("🎉 등록 완료! 정식 출시 때 가장 먼저 연락드리겠습니다.")
