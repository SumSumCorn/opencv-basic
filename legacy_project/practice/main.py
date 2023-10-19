import streamlit as st
import math
import mediapipe as mp
import time
import cv2


def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))


st.title("가위바위보 게임")

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

activate_button = st.button("run")


with st.sidebar:
    st.selectbox("game options", ("play with Computers", "play with Humans"))

if activate_button:
    ret, frame = cap.read()

    if not ret:
        st.write("Camera error.")
        st.stop()
