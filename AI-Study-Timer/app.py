import streamlit as st

st.set_page_config(page_title="AI 맞춤형 학습 타이머", page_icon="⏱️", layout="wide")

st.title("AI 피드백 학습 타이머")
st.markdown("""
이 프로그램은**제미나이(Gemini) API**를 활용하여 만들었습니다.

👈 좌측 사이드바 메뉴를 통해 이동하세요.
 **로그인 및 회원가입**을 먼저 진행하세요.
""")

# 사용자 정보 전역 세션 초기화
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_mode" not in st.session_state:
    st.session_state.user_mode = None
if "user_subjects" not in st.session_state:
    st.session_state.user_subjects = []
