import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase() -> Client:
    # secrets.toml에 저장해둔 값들을 불러옵니다.
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)
