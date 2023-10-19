# mediapipe + rps 게임 

import cv2
import sys
import mediapipe as mp
import math
import random

def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera is not opened")
    sys.exit(1)

hands = mp_hands.Hands()

while True:
    res, frame = cap.read()
    
    if not res:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )
            
            points = hand_landmarks.landmark
            fingers = 0
            
            if distance(points[4], points[9]) > distance(points[3], points[9]):
                fingers += 1
            
            for i in range(8, 21, 4):
                if distance(points[i], points[0]) > distance(points[i - 1], points[0]):
                    fingers += 1
            
            if fingers == 0:
                hand_shape = "rock"
            elif fingers == 2:
                hand_shape = "scissors"
            elif fingers == 5:
                hand_shape = "paper"
            else:
                hand_shape = ""
            
            cv2.putText(
                frame,
                hand_shape,
                (int(points[12].x * frame.shape[1]), int(points[12].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                3,
                (0, 255, 0),
                5,
            )

            # Determine winner
            if hand_shape:
                if hand_shape == computer_choice:
                    result = "It's a tie!"
                elif (hand_shape == 'rock' and computer_choice == 'scissors') or \
                     (hand_shape == 'scissors' and computer_choice == 'paper') or \
                     (hand_shape == 'paper' and computer_choice == 'rock'):
                    result = "You win!"
                else:
                    result = "Computer wins!"

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
                    result,
                    (50, 100),
                    cv2.FONT_HERSHEY_COMPLEX,
                    1,
                    (255, 0, 0),
                    2,
                )

    cv2.imshow("MediaPipe Hands", frame)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()
