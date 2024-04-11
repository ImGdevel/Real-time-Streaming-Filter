from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2

class ObjectDetector:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.names = self.model.names
    
    def detect(self, image):
        results = self.model.predict(image, show=False)
        boxes = results[0].boxes.xyxy.cpu().tolist()
        clss = results[0].boxes.cls.cpu().tolist()
        return boxes, clss

class VideoProcessor:
    def __init__(self, detector, blur_ratio=50):
        self.detector = detector
        self.blur_ratio = blur_ratio
        self.cap = cv2.VideoCapture(0)
        assert self.cap.isOpened(), "Error reading video file"
        self.w, self.h, self.fps = (int(self.cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
        self.video_writer = cv2.VideoWriter("object_blurring_output.avi", cv2.VideoWriter_fourcc(*'mp4v'), self.fps, (self.w, self.h))
    
    def process(self):
        while self.cap.isOpened():
            success, im0 = self.cap.read()
            if not success:
                print("Video frame is empty or video processing has been successfully completed.")
                break
            
            boxes, clss = self.detector.detect(im0)
            annotator = Annotator(im0, line_width=2, example=self.detector.names)

            if boxes:
                for box, cls in zip(boxes, clss):
                    if self.detector.names[cls] == 'Human face':
                        annotator.box_label(box, color=colors(int(cls), True), label=self.detector.names[int(cls)])
                        obj = im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                        blur_obj = cv2.blur(obj, (self.blur_ratio, self.blur_ratio))
                        im0[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj
            
            cv2.imshow("ultralytics", im0)
            self.video_writer.write(im0)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        self.cap.release()
        self.video_writer.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    detector = ObjectDetector("models/yolov8n-oiv7.pt")
    processor = VideoProcessor(detector)
    processor.process()
