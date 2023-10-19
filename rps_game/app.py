###
### 설명 :
###
import streamlit as st
import cv2
import mediapipe as mp


from utils.states import init, reset, toggle
from utils.camera import game_mode, normal_mode
from utils.ui import before_start, after_start

st.title("가위바위보 게임!!")

init()

### 설명 :
###
###OpenCV capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    st.error("Camera is not opened")
    st.stop()


if st.session_state.is_started:
    game_mode(cap)
else:
    normal_mode(cap)

cap.release()
