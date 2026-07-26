import streamlit as st
from utils import init_supabase

st.set_page_config(page_title="로그인/회원가입", page_icon="👤")

supabase = init_supabase()

menu = st.radio("선택하세요", ["로그인", "회원가입"])

if menu == "회원가입":
    st.header("👤 회원가입")
    with st.form("signup_form"):
        new_id = st.text_input("아이디")
        new_pw = st.text_input("비밀번호", type="password")
        mode = st.radio("피드백 모드 선택", ["일반 모드 (통계만 제공)", "AI 모드 (통계 + 맞춤형 피드백)"])
        st.info("가장 중요하게 생각하는 과목부터 순서대로 적어주세요. (예: 수학, 영어, 국어)")
        subjects_input = st.text_input("과목 목록 (쉼표로 구분)")
        
        submitted = st.form_submit_button("가입하기")
        if submitted:
            if not new_id or not new_pw or not subjects_input:
                st.error("모든 항목을 입력해주세요.")
            else:
                # 1. 아이디 중복 확인
                res = supabase.table("users").select("*").eq("user_id", new_id).execute()
                if len(res.data) > 0:
                    st.error("이미 존재하는 아이디입니다.")
                else:
                    # 2. 수파베이스 users 테이블에 데이터 넣기
                    supabase.table("users").insert({
                        "user_id": new_id,
                        "password": new_pw,
                        "mode": mode,
                        "subjects": subjects_input
                    }).execute()
                    st.success("회원가입 완료! 로그인 탭으로 이동해서 로그인해주세요.")

elif menu == "로그인":
    st.header("🔑 로그인")
    login_id = st.text_input("아이디")
    login_pw = st.text_input("비밀번호", type="password")
    
    if st.button("로그인"):
        res = supabase.table("users").select("*").eq("user_id", login_id).execute()
        if len(res.data) == 0:
            st.error("존재하지 않는 아이디입니다.")
        else:
            user_data = res.data[0]
            if user_data["password"] == login_pw:
                # 세션에 로그인 정보 저장
                st.session_state.logged_in_user = login_id
                st.session_state.user_mode = user_data["mode"]
                st.session_state.user_subjects = [s.strip() for s in user_data["subjects"].split(",")]
                st.success(f"로그인 성공! 환영합니다, {login_id}님.")
            else:
                st.error("비밀번호가 틀렸습니다.")
                
# 로그아웃 버튼
if st.session_state.logged_in_user:
    st.markdown("---")
    if st.button("로그아웃"):
        st.session_state.logged_in_user = None
        st.session_state.user_mode = None
        st.session_state.user_subjects = []
        st.rerun()
