import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from utils import init_supabase

st.set_page_config(page_title="피드백 통계", page_icon="📊", layout="wide")

if st.session_state.get("logged_in_user") is None:
    st.warning("로그인이 필요한 페이지입니다. 좌측 메뉴에서 로그인을 먼저 해주세요.")
    st.stop()

supabase = init_supabase()
user_id = st.session_state.logged_in_user
user_mode = st.session_state.user_mode
user_subjects = st.session_state.user_subjects

st.header("📊 피드백 공간")
st.write(f"현재 설정된 모드: **{user_mode}**")
st.write(f"나의 과목 우선순위 (1순위부터): **{', '.join(user_subjects)}**")
st.markdown("---")

# 1. 수파베이스에서 내 데이터만 불러오기
res = supabase.table("study_logs").select("*").eq("user_id", user_id).execute()
logs = res.data

if not logs:
    st.warning("아직 공부 기록이 없습니다. 타이머를 사용해 기록을 남겨보세요!")
else:
    df = pd.DataFrame(logs)
    
    st.subheader("📈 내 공부 통계")
    col1, col2 = st.columns(2)
    
    subject_totals = df.groupby('subject')['minutes'].sum().reset_index()
    
    with col1:
        fig_pie = px.pie(subject_totals, values='minutes', names='subject', title='과목별 공부 비율 (원 그래프)')
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col2:
        fig_bar = px.bar(subject_totals, x='subject', y='minutes', title='과목별 누적 공부 시간 (막대 그래프)', color='subject')
        st.plotly_chart(fig_bar, use_container_width=True)

    # 2. AI 모드일 경우에만 피드백 활성화
    if "AI" in user_mode:
        st.markdown("---")
        st.subheader("🤖 Gemini 맞춤형 피드백")
        
        try:
            # secrets.toml에서 제미나이 키 가져오기
            api_key = st.secrets["gemini"]["api_key"]
            genai.configure(api_key=api_key)
            
            if st.button("AI 피드백 생성하기"):
                with st.spinner("데이터를 분석하고 피드백을 작성 중입니다..."):
                    priorities_str = ", ".join(user_subjects)
                    study_data_str = subject_totals.to_string(index=False)
                    
                    prompt = f"""
                    너는 학생의 공부 데이터를 분석해주는 날카롭고 친절한 AI 코치야.
                    
                    [학생 정보 및 데이터]
                    - 학생이 설정한 과목별 우선순위(앞일수록 중요): {priorities_str}
                    - 현재까지 과목별 누적 공부 시간(분): 
                    {study_data_str}
                    
                    [요구사항]
                    1. 학생이 설정한 '우선순위'와 '실제 공부 시간'을 비교 분석해줘.
                    2. 중요도가 높은데 시간이 부족한 과목이 있는지(편식), 우선순위가 낮은데 시간을 너무 많이 쏟은 과목이 있는지 파악해줘.
                    3. 앞으로 어떤 과목을 늘리고 어떤 과목을 줄여야 할지 구체적인 피드백을 제공해줘.
                    """
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    response = model.generate_content(prompt)
                    st.info(response.text)
        except KeyError:
            st.error("secrets.toml 파일에 제미나이 API 키가 설정되지 않았습니다.")
        except Exception as e:
            st.error(f"AI 호출 중 오류가 발생했습니다: {e}")
