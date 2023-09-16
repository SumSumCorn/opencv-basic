import cv2
import mediapipe as mp
import math
import numpy as np
import streamlit as st
import sys


def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def main():
    st.title("Hand Pose to Control Video Playback")

    hands = mp_hands.Hands(max_num_hands=1)

    cap = cv2.VideoCapture(0)
    video = cv2.VideoCapture("Boat.mp4")

    if not cap.isOpened():
        st.error("Camera is not opened")
        sys.exit(1)

    if not video.isOpened():
        st.error("Video is not opened")
        sys.exit(1)

    end = video.get(cv2.CAP_PROP_FRAME_COUNT)
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)

    video_res, video_frame = video.read()

    stframe1 = st.empty()
    stframe2 = st.empty()

    while True:
        res, frame = cap.read()

        if not res:
            st.error("Camera error")
            break

        frame = cv2.flip(frame, 1)
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        hand_shape = ""
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            points = hand_landmarks.landmark

            fingers = [0, 0, 0, 0, 0]

            if distance(points[4], points[9]) > distance(points[3], points[9]):
                fingers[0] = 1

            for i in range(1, 5):
                if distance(points[4 * (i + 1)], points[0]) > distance(
                    points[4 * (i + 1) - 1], points[0]
                ):
                    fingers[i] = 1

            if fingers == [0, 0, 0, 0, 0]:
                hand_shape = "rock"
            elif distance(points[4], points[8]) < 0.1 and fingers[2:] == [1, 1, 1]:
                pos = int(np.interp(points[8].x * w, (50, w - 50), (1, end - 1)))
                video.set(cv2.CAP_PROP_POS_FRAMES, pos)
                hand_shape = "OK"

        stframe1.image(frame, channels="BGR")
        stframe2.image(video_frame, channels="BGR")

        if hand_shape != "rock" and video.get(cv2.CAP_PROP_POS_FRAMES) != end:
            video_res, video_frame = video.read()
            if not video_res:
                st.error("Video error")
                break


if __name__ == "__main__":
    main()
