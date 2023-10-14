import cv2
import sys
import mediapipe as mp
import math
import random
import time

# 두 점 사이의 거리를 계산하는 함수
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))

# 메인 코드를 실행하기 위한 함수
def main():
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera is not opened")
        sys.exit(1)

    hands = mp_hands.Hands()
    initialize_game_variables()

    while True:
        res, frame = capture_frame(cap)
        if not res:
            print("Camera error")
            break
        
        frame, results = process_frame(frame, hands)
        play_game(frame, results)

        show_frame(frame)
        if check_exit_condition():
            break

    cleanup(cap)

# 게임 변수를 초기화하는 함수
def initialize_game_variables():
    global input_start_time, output_start_time, final_hand_shape, result, user_score, computer_score
    input_start_time = None
    output_start_time = None
    final_hand_shape = ""
    result = ""
    user_score = 0
    computer_score = 0

# 카메라에서 프레임을 캡처하는 함수
def capture_frame(cap):
    res, frame = cap.read()
    frame = cv2.flip(frame, 1)
    return res, frame

# 프레임을 처리하는 함수
def process_frame(frame, hands):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    return frame, results

# 게임을 진행하는 함수
def play_game(frame, results):
    global input_start_time, output_start_time, final_hand_shape, result, user_score, computer_score

    if input_start_time is None:
        input_start_time = time.time()

    elapsed_input_time = time.time() - input_start_time
    remaining_input_time = 3 - int(elapsed_input_time)

    if elapsed_input_time <= 3:
        play_input_phase(frame, results, remaining_input_time)
    else:
        play_output_phase(frame)

# 입력 단계를 진행하는 함수
def play_input_phase(frame, results, remaining_input_time):
    global final_hand_shape
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
            draw_hand_landmarks(frame, hand_landmarks)
            final_hand_shape = detect_hand_shape(hand_landmarks, frame)

# 출력 단계를 진행하는 함수
def play_output_phase(frame):
    global output_start_time, result, user_score, computer_score
    if output_start_time is None:
        output_start_time = time.time()
        decide_winner()

    elapsed_output_time = time.time() - output_start_time
    remaining_output_time = 3 - int(elapsed_output_time)

    if elapsed_output_time <= 3:
        display_output(frame, remaining_output_time)

# 손의 모양을 탐지하는 함수
def detect_hand_shape(hand_landmarks, frame):
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
    return hand_shape

# 손의 랜드마크를 그리는 함수
def draw_hand_landmarks(frame, hand_landmarks):
    mp_drawing.draw_landmarks(
        frame,
        hand_landmarks,
        mp_hands.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style(),
    )

# 승자를 결정하는 함수
def decide_winner():
    global result, user_score, computer_score
    computer_choice = random.choice(['rock', 'paper', 'scissors'])
    if final_hand_shape == computer_choice:
        result = "It's a tie!"
    elif (final_hand_shape == 'rock' and computer_choice == 'scissors') or \
         (final_hand_shape == 'scissors' and computer_choice == 'paper') or \
         (final_hand_shape == 'paper' and computer_choice == 'rock'):
        result = "You win!"
        user_score += 1
    else:
        result = "Computer wins!"
        computer_score += 1

# 출력을 화면에 표시하는 함수
def display_output(frame, remaining_output_time):
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
        result,
        (50, 100),
        cv2.FONT_HERSHEY_COMPLEX,
        1,
        (255, 0, 0),
        2,
    )

# 프레임을 화면에 표시하는 함수
def show_frame(frame):
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

# 종료 조건을 확인하는 함수
def check_exit_condition():
    key = cv2.waitKey(5) & 0xFF
    return key == 27

# 자원을 정리하는 함수
def cleanup(cap):
    cv2.destroyAllWindows()
    cap.release()

if __name__ == "__main__":
    main()
