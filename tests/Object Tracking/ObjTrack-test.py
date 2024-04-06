import cv2
import numpy as np

# 웹캠 비디오 스트림 열기
cap = cv2.VideoCapture(0)

# 첫 번째 프레임 읽기
ret, frame = cap.read()

# 추적 영역 선택
bbox = cv2.selectROI("Select Object", frame, fromCenter=False, showCrosshair=True)
cv2.destroyAllWindows()

# 추적을 위한 초기 설정
roi = frame[int(bbox[1]):int(bbox[1]+bbox[3]), int(bbox[0]):int(bbox[0]+bbox[2])]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# MeanShift 파라미터 설정
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    
    # MeanShift 알고리즘 적용
    ret, bbox = cv2.meanShift(dst, (bbox[0], bbox[1], bbox[2], bbox[3]), term_criteria)
    
    # 추적 결과를 프레임에 표시
    x, y, w, h = bbox
    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow('Tracking', frame)
    
    if cv2.waitKey(60) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
