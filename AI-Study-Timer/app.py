import streamlit as st

st.set_page_config(page_title="AI 맞춤형 학습 타이머", page_icon="⏱️", layout="wide")

st.title("📚 AI 맞춤형 학습 타이머에 오신 것을 환영합니다!")
st.markdown("""
이 프로젝트는 **스트림릿(Streamlit)**과 **수파베이스(Supabase)**, 그리고 **제미나이(Gemini) AI**를 활용하여 만들어졌습니다.

👈 좌측 사이드바 메뉴를 통해 이동해주세요.
1. **로그인 및 회원가입**을 먼저 진행해주세요.
2. **공부 타이머**로 과목별 학습 시간을 기록하세요.
3. **AI 피드백 통계**에서 데이터 시각화 및 맞춤형 피드백을 받아보세요.
""")

# 사용자 정보 전역 세션 초기화
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None
if "user_mode" not in st.session_state:
    st.session_state.user_mode = None
if "user_subjects" not in st.session_state:
    st.session_state.user_subjects = []
