import cv2
import sys
import mediapipe as mp
import math
import random
import time


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

input_start_time = None
output_start_time = None
final_hand_shape = ""
result = ""
user_score = 0
computer_score = 0

while True:
    res, frame = cap.read()

    if not res:
        print("Camera error")
        break

    frame = cv2.flip(frame, 1)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if input_start_time is None:
        input_start_time = time.time()

    elapsed_input_time = time.time() - input_start_time
    remaining_input_time = 3 - int(elapsed_input_time)

    if elapsed_input_time <= 3:
        cv2.putText(
            frame,
            f"Time remaining: {remaining_input_time}",
            (400, 50),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (255, 0, 0),
            2,
        )

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
                    if distance(points[i], points[0]) > distance(
                        points[i - 1], points[0]
                    ):
                        fingers += 1

                if fingers == 0:
                    final_hand_shape = "rock"
                elif fingers == 2:
                    final_hand_shape = "scissors"
                elif fingers == 5:
                    final_hand_shape = "paper"
                else:
                    final_hand_shape = ""

                cv2.putText(
                    frame,
                    final_hand_shape,
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
        if output_start_time is None:
            computer_choice = random.choice(["rock", "paper", "scissors"])
            if final_hand_shape == computer_choice:
                result = "It's a tie!"
            elif (
                (final_hand_shape == "rock" and computer_choice == "scissors")
                or (final_hand_shape == "scissors" and computer_choice == "paper")
                or (final_hand_shape == "paper" and computer_choice == "rock")
            ):
                result = "You win!"
                user_score += 1
            else:
                result = "Computer wins!"
                computer_score += 1

            output_start_time = time.time()

        elapsed_output_time = time.time() - output_start_time
        remaining_output_time = 3 - int(elapsed_output_time)

        if elapsed_output_time <= 3:
            cv2.putText(
                frame,
                f"Time remaining: {remaining_output_time}",
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
                result,
                (50, 100),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 0, 0),
                2,
            )
        else:
            input_start_time = None
            output_start_time = None

    cv2.putText(
        frame,
        f"Score: User - {user_score}, Computer - {computer_score}",
        (50, 400),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (0, 255, 0),
        2,
    )

    cv2.imshow("MediaPipe Hands", frame)
    key = cv2.waitKey(5) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()
