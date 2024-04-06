import cv2

class VideoProcessor:
    def __init__(self):
        self.video_cap = cv2.VideoCapture(0)
        # 얼굴 검출을 위한 Haar 분류기 초기화
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def get_frame(self):
        """ 현재 비디오 프레임을 반환 """
        ret, frame = self.video_cap.read()
        if ret:
            # BGR 포맷을 RGB 포맷으로 변환하여 반환
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            return None

    def mosaic_face(self, frame):
        """ 얼굴 부분을 모자이크 처리 """
        mosaic_frame = frame.copy()
        gray = cv2.cvtColor(mosaic_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 2, 5)
        
        #검출된 얼굴 부분을 모자이크 처리
        for (x, y, w, h) in faces:
            roi = mosaic_frame[y:y+h, x:x+w]
            roi = cv2.resize(roi, (w//15, h//15), interpolation=cv2.INTER_LINEAR)
            roi = cv2.resize(roi, (w, h), interpolation=cv2.INTER_NEAREST)
            mosaic_frame[y:y+h, x:x+w] = roi
        
        return mosaic_frame

    def convert_to_grayscale(self, frame):
        # 이미지를 그레이스케일로 변환
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 그레이스케일 이미지를 RGB 포맷으로 변환하여 반환
        return cv2.cvtColor(frame_gray, cv2.COLOR_GRAY2RGB)
    
    def invert_colors(self, frame):
        # 이미지의 색상을 반전시킴
        frame_inverted = cv2.bitwise_not(frame)
        # 반전된 이미지를 RGB 포맷으로 변환하여 반환
        return cv2.cvtColor(frame_inverted, cv2.COLOR_BGR2RGB)
