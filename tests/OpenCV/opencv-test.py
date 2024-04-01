import cv2

def detect_faces():
    # 웹캠을 켭니다.
    cap = cv2.VideoCapture(0)

    # 얼굴 인식을 위해 얼굴 검출기를 로드합니다.
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    while True:
        # 웹캠으로부터 영상을 받아옵니다.
        ret, frame = cap.read()

        if not ret:
            break

        # 영상을 회색으로 변환합니다.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 얼굴을 검출합니다.
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # 검출된 얼굴 주위에 사각형을 그립니다.
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 결과 영상을 화면에 출력합니다.
        cv2.imshow('Face Detection', frame)

        # 'q'를 누르면 종료합니다.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 웹캠을 끕니다.
    cap.release()
    cv2.destroyAllWindows()

# 웹캠으로부터 얼굴을 인식합니다.
detect_faces()