import streamlit as st
from utils.states import toggle, reset


def after_start():
    with st.container():
        col1, col2, col3 = st.columns(3)
        col1.metric("이긴횟수", st.session_state.user_score)
        col2.metric("진 횟수", st.session_state.computer_score)
        col3.metric("전체 판수", st.session_state.total_count)
        col1.button("다시 도전?", key="resume_button", type="primary", on_click=toggle)
        col3.button("종료", key="reset_button", on_click=reset)


def before_start():
    with st.empty():
        st.button("게임시작", key="start_button", type="primary", on_click=toggle)
