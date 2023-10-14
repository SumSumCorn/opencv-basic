import cv2

# 웹캠 초기화
cap = cv2.VideoCapture(0)

while True:
    # 프레임 캡처
    ret, img = cap.read()
    
    if not ret:
        print("Failed to grab frame.")
        break

    # 텍스트 추가
    cv2.putText(img, 'Webcam Text', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # 이미지 출력
    cv2.imshow('Webcam Frame', img)

    # 'q' 키를 누르면 루프 탈출
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제
cap.release()
cv2.destroyAllWindows()
