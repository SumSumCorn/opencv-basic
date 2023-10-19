###
### 설명 :
###
import streamlit as st
import cv2
import mediapipe as mp
import math
import random
import time


###
### 설명 :
###
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))


###
### 설명 :
###
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

st.title("가위바위보 게임!!")

# Initial states
###
### 설명 :
###
if "input_start_time" not in st.session_state:
    st.session_state.input_start_time = None
if "output_start_time" not in st.session_state:
    st.session_state.output_start_time = None
if "final_hand_shape" not in st.session_state:
    st.session_state.final_hand_shape = ""
if "result" not in st.session_state:
    st.session_state.result = ""
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

###
### 설명 :
###
###OpenCV capture
cap = cv2.VideoCapture(0)
###
### 설명 :
###
if not cap.isOpened():
    st.error("Camera is not opened")
    st.stop()
###
### 설명 :
###
hands = mp_hands.Hands()

###
### 설명 :
###
video_slot = st.empty()

###
### 설명:
###
while True:
    res, frame = cap.read()
    ###
    ### 설명 :
    ###
    if not res:
        st.error("Camera error")
        break
    ###
    ### 설명 :
    ###
    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    ###
    ### 설명 :
    ###
    if st.session_state.input_start_time is None:
        st.session_state.input_start_time = time.time()
    ###
    ### 설명 :
    ###
    elapsed_input_time = time.time() - st.session_state.input_start_time
    remaining_input_time = 3 - int(elapsed_input_time)
    ###
    ### 설명 :
    ###
    if elapsed_input_time <= 3:
        ###
        ### 설명 :
        ###
        cv2.putText(
            frame,
            f"Time remaining: {remaining_input_time}",
            (400, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            2,
        )
        ###
        ### 설명 :
        ###
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                ###
                ### 설명 :
                ###
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style(),
                )

            points = hand_landmarks.landmark
            fingers = 0
            ###
            ### 설명 :
            ###
            if distance(points[4], points[9]) > distance(points[3], points[9]):
                fingers += 1
            ###
            ### 설명 :
            ###
            for i in range(8, 21, 4):
                if distance(points[i], points[0]) > distance(points[i - 1], points[0]):
                    fingers += 1

            if fingers == 0:
                st.session_state.final_hand_shape = "rock"
            elif fingers == 2:
                st.session_state.final_hand_shape = "scissors"
            elif fingers == 5:
                st.session_state.final_hand_shape = "paper"
            else:
                st.session_state.final_hand_shape = ""
            ###
            ### 설명 :
            ###
            cv2.putText(
                frame,
                st.session_state.final_hand_shape,
                (
                    int(points[12].x * frame.shape[1]),
                    int(points[12].y * frame.shape[0]),
                ),
                cv2.FONT_HERSHEY_COMPLEX,
                3,
                (0, 255, 0),
                5,
            )

    else:
        ###
        ### 설명 :
        ###
        if st.session_state.output_start_time is None:
            ###
            ### 설명 :
            ###
            computer_choice = random.choice(["rock", "paper", "scissors"])
            if st.session_state.final_hand_shape == computer_choice:
                st.session_state.result = "It's a tie!"
            elif (
                (
                    st.session_state.final_hand_shape == "rock"
                    and computer_choice == "scissors"
                )
                or (
                    st.session_state.final_hand_shape == "scissors"
                    and computer_choice == "paper"
                )
                or (
                    st.session_state.final_hand_shape == "paper"
                    and computer_choice == "rock"
                )
            ):
                st.session_state.result = "You win!"
                st.session_state.user_score += 1
            else:
                st.session_state.result = "Computer wins!"
                st.session_state.computer_score += 1

            st.session_state.output_start_time = time.time()

        elapsed_output_time = time.time() - st.session_state.output_start_time
        remaining_output_time = 3 - int(elapsed_output_time)

        if elapsed_output_time <= 3:
            cv2.putText(
                frame,
                f"{remaining_output_time}",
                (400, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
            )

            cv2.putText(
                frame,
                f"Computer chose: {computer_choice}",
                (50, 50),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (0, 255, 255),
                2,
            )

            cv2.putText(
                frame,
                st.session_state.result,
                (50, 100),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
            )
        else:
            st.session_state.input_start_time = None
            st.session_state.output_start_time = None
    ###
    ### 설명 :
    ###
    cv2.putText(
        frame,
        f"Score: User - {st.session_state.user_score}, Computer - {st.session_state.computer_score}",
        (50, 400),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    ###
    ### 설명:
    ###
    video_slot.image(frame, channels="BGR")

###
### 설명 :
###
cap.release()
