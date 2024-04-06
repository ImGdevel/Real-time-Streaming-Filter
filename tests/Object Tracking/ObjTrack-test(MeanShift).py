import cv2
import numpy as np

# 웹캠 비디오 스트림 열기
cap = cv2.VideoCapture(0)

# 얼굴 검출을 위한 Haar Cascades 분류기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# 추적을 위한 초기 설정 변수
track_window = None
roi_hist = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 얼굴 검출
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in faces:
        # 얼굴 영역을 추적 영역으로 설정
        track_window = (x, y, w, h)
        
        # 추적을 위한 초기 설정
        roi = frame[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
        cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
        
        break
    
    # 추적 설정이 완료되면 MeanShift 알고리즘을 사용하여 객체를 추적
    if track_window is not None and roi_hist is not None:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
        
        # MeanShift 알고리즘 적용
        ret, track_window = cv2.meanShift(dst, track_window, (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1))
        
        # 추적 결과를 프레임에 표시
        x, y, w, h = track_window
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('Face Tracking', frame)
    
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
