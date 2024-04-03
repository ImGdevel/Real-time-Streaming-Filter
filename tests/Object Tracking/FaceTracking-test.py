import cv2

# 이미지 로드
image_path = "image/person.jpg"
person_image = cv2.imread(image_path)

# 웹캠 영상 받아오기
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    cv2.imshow("Webcam", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# YOLO 가중치 파일과 설정 파일 경로
yolo_weights = "yolov3.weights"
yolo_cfg = "yolov3.cfg"
yolo_classes = "coco.names"

# YOLO 네트워크 로딩
net = cv2.dnn.readNetFromDarknet(yolo_cfg, yolo_weights)
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# 이미지 로딩 및 전처리
blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
net.setInput(blob)
outs = net.forward(output_layers)

# 정보를 화면에 표시
for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        
        if confidence > 0.5 and class_id == 0:  # 0번 클래스는 사람
            # 얼굴 영역 추출
            box = detection[0:4] * np.array([w, h, w, h])
            (x, y, w, h) = box.astype("int")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imshow("Face Detection", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()