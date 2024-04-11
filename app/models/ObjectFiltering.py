from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2


class ObjectFiltering:
    origin = YOLO("models/yolov8n-oiv7.pt")   # 기존 범용적으로 인식하는 모델
    custom = YOLO("models/bad.pt")   # 유해 객체 인식을 위해 사용자 정의 데이터셋을 통해 학습된 모델
    orgNames = None # 범용 모델의 라벨이 들어있다.
    custNames = None # 사용자 정의 모델의 라벨이 들어있다.
    def __init__(self):
        self.orgNames = self.origin.names
        self.custNames = self.custom.names
        
        
    def objectDetect(self, img, filterObjects):
        results = self.origin.predict(img, show=False)  # 주어진 이미지에 대한 범용모델의 예측결과를 저장한다.
        results2 = self.custom.predict(img, show=False) # 주어진 이미지에 대한 사용자 모델의 예측결과를 저장한다.
        orgBoxes = results[0].boxes.xyxy.cpu().tolist() # 인식된 객체의 좌표를 저장한다.
        orgClss = results[0].boxes.cls.cpu().tolist()   # 인식된 객체의 라벨정보를 저장한다.
        custBoxes = results2[0].boxes.xyxy.cpu().tolist()   
        custClss = results2[0].boxes.cls.cpu().tolist()     
        annotator = Annotator(img, line_width=2, example=self.orgNames)
        boxesList = []      # 필터링 대상 객체들의 좌표 리스트를 저장하는 리스트 객체
        
        if orgBoxes is not None:
            for box, cls in zip(orgBoxes, orgClss):
                if filterObjects[self.orgNames[cls]] == 1:  # 필터링 대상 객체라면 1 
                    annotator.box_label(box, color=colors(int(cls), True), label=self.orgNames[int(cls)])

                    # obj = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
                    # blur_obj = cv2.blur(obj, (blur_ratio, blur_ratio))
                    # img[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj
                    boxesList.append(box) 
        if custBoxes is not None:
            for box, cls in zip(custBoxes, custClss):
                if filterObjects[self.custNames[cls]] == 1: # 필터링 대상 객체라면 1
                    annotator.box_label(box, color=colors(int(cls), True), label=self.custNames[int(cls)])

                    
                    boxesList.append(box)
        return boxesList

# cap = cv2.VideoCapture(0)
# assert cap.isOpened(), "Error reading video file"
# w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

# # Blur ratio
# blur_ratio = 50

# # Video writer
# video_writer = cv2.VideoWriter("object_blurring_output.avi",
#                                cv2.VideoWriter_fourcc(*'mp4v'),
#                                fps, (w, h))



# while cap.isOpened():
#     success, img = cap.read()
#     if not success:
#         print("Video frame is empty or video processing has been successfully completed.")
#         break
#     temp = obj.objectDetect(img, testDict)
#     cv2.imshow("ultralytics", img)
#     video_writer.write(img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# video_writer.release()
# cv2.destroyAllWindows()