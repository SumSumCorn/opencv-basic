import streamlit as st
import cv2
import mediapipe as mp
import math
import numpy as np
from PIL import Image


# Distance calculation function
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))


# Initialize mediapipe components
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

st.title("Handprint Recognition")
run = st.checkbox("Run")

FRAME_WINDOW = st.image([], channels="BGR")

cap = cv2.VideoCapture(0)

hands = mp_hands.Hands()

while run:
    ret, frame = cap.read()

    if not ret:
        st.warning("Camera error.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            points = hand_landmarks.landmark
            fingers = 0

            if distance(points[4], points[9]) > distance(points[3], points[9]):
                fingers += 1

            for i in range(8, 21, 4):
                if distance(points[i], points[0]) > distance(points[i - 1], points[0]):
                    fingers += 1

            if fingers == 0:
                hand_shape = "Rock"
            elif fingers == 2:
                hand_shape = "Scissors"
            elif fingers == 5:
                hand_shape = "Paper"
            else:
                hand_shape = ""

            cv2.putText(
                frame,
                hand_shape,
                (
                    int(points[12].x * frame.shape[1]),
                    int(points[12].y * frame.shape[0]),
                ),
                cv2.FONT_HERSHEY_COMPLEX,
                3,
                (0, 255, 0),
                5,
            )

    FRAME_WINDOW.image(frame, channels="BGR")

cap.release()
cv2.destroyAllWindows()
