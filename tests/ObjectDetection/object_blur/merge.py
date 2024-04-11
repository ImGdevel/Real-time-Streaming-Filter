from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2

# model = YOLO("yolov8n.pt")
model = YOLO("models/yolov8n-oiv7.pt")
bad = YOLO("runs/detect/train21/weights/best.pt")
names = model.names
names[601] = "smoke"

cap = cv2.VideoCapture(0)
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# Blur ratio
blur_ratio = 50

# Video writer
video_writer = cv2.VideoWriter("object_blurring_output.avi",
                               cv2.VideoWriter_fourcc(*'mp4v'),
                               fps, (w, h))

while cap.isOpened():
    success, im0 = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    results = model.predict(im0, show=False)
    results2 = bad.predict(im0, show=False)
    boxes = results[0].boxes.xyxy.cpu().tolist()
    clss = results[0].boxes.cls.cpu().tolist()
    boxes2 = results2[0].boxes.xyxy.cpu().tolist()
    clss2 = results2[0].boxes.cls.cpu().tolist()
    annotator = Annotator(im0, line_width=2, example=names)

    if boxes is not None:
        for box, cls in zip(boxes, clss):
            if names[cls] == 'Human face':
                annotator.box_label(box, color=colors(int(cls), True), label=names[int(cls)])

                obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                blur_obj = cv2.blur(obj, (blur_ratio, blur_ratio))

                im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj
    if boxes2 is not None:
        for box, cls in zip(boxes2, clss2):
            if names[601+cls] == 'smoke':
                annotator.box_label(box, color=colors(int(cls), True), label=names[601+int(cls)])

                obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                blur_obj = cv2.blur(obj, (blur_ratio, blur_ratio))

                im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj


    cv2.imshow("ultralytics", im0)
    video_writer.write(im0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()