import streamlit as st
import time
import datetime
from utils import init_supabase

st.set_page_config(page_title="공부 타이머", page_icon="⏱️")

if st.session_state.get("logged_in_user") is None:
    st.warning("로그인이 필요한 페이지입니다. 좌측 메뉴에서 로그인을 먼저 해주세요.")
    st.stop()

supabase = init_supabase()
user_id = st.session_state.logged_in_user
subjects = st.session_state.user_subjects

st.header(f"⏱️ {user_id}님의 공부 타이머")

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "current_subject" not in st.session_state:
    st.session_state.current_subject = None

selected_subject = st.selectbox("공부할 과목 선택", subjects, disabled=st.session_state.timer_running)

col1, col2 = st.columns(2)
with col1:
    st.subheader("타이머 조작")
    if not st.session_state.timer_running:
        if st.button("▶️ 공부 시작"):
            st.session_state.timer_running = True
            st.session_state.start_time = time.time()
            st.session_state.current_subject = selected_subject
            st.rerun()
    else:
        elapsed_time = time.time() - st.session_state.start_time
        mins, secs = divmod(int(elapsed_time), 60)
        hours, mins = divmod(mins, 60)
        st.warning(f"⏳ 진행 중: {hours:02d}:{mins:02d}:{secs:02d} ({st.session_state.current_subject})")
        
        if st.button("⏹️ 공부 종료 및 저장"):
            st.session_state.timer_running = False
            total_minutes = elapsed_time / 60
            
            # 수파베이스 study_logs 테이블에 저장
            supabase.table("study_logs").insert({
                "user_id": user_id,
                "log_date": str(datetime.date.today()),
                "subject": st.session_state.current_subject,
                "minutes": round(total_minutes, 2)
            }).execute()
            
            st.success(f"🎉 {st.session_state.current_subject} 과목 {round(total_minutes, 2)}분 기록 완료!")
            st.session_state.start_time = None
            st.session_state.current_subject = None
            st.rerun()

with col2:
    st.subheader("수동 기록 추가")
    st.info("타이머를 깜빡했다면 수동으로 기록하세요.")
    manual_date = st.date_input("날짜 선택")
    manual_mins = st.number_input("공부 시간 (분)", min_value=1)
    if st.button("수동 기록 저장"):
        supabase.table("study_logs").insert({
            "user_id": user_id,
            "log_date": str(manual_date),
            "subject": selected_subject,
            "minutes": manual_mins
        }).execute()
        st.success("저장되었습니다.")
