import streamlit as st


def toggle():
    st.session_state.is_started = not st.session_state.is_started


def reset():
    st.session_state.is_started = False
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.session_state.total_count = 0


def init():
    # Initial states
    ###
    ### 설명 :
    ###

    if "is_started" not in st.session_state:
        st.session_state.is_started = False

    if "input_start_time" not in st.session_state:
        st.session_state.input_start_time = None
    if "output_start_time" not in st.session_state:
        st.session_state.output_start_time = None

    if "final_hand_shape" not in st.session_state:
        st.session_state.final_hand_shape = ""
    if "result" not in st.session_state:
        st.session_state.result = ""

    if "total_count" not in st.session_state:
        st.session_state.total_count = 0
    if "user_score" not in st.session_state:
        st.session_state.user_score = 0
    if "computer_score" not in st.session_state:
        st.session_state.computer_score = 0
