from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from models.ModelManager import ModelManager
import cv2

class ObjectDetect:
    """
    YOLO 모델을 사용한 객체 탐지를 위한 클래스입니다.

    속성:
        origin (YOLO): 일반 객체 탐지를 위한 YOLO 모델입니다.
        custom (YOLO): 사용자 정의 객체 탐지를 위한 YOLO 모델입니다.
        orgNames (list): 일반 모델에 의해 탐지된 객체의 라벨입니다.
        custNames (list): 사용자 정의 모델에 의해 탐지된 객체의 라벨입니다.

    메서드:
        __init__: YOLO 모델과 그들의 라벨로 ObjectDetect 클래스를 초기화합니다.
        orgDetect: 일반 YOLO 모델을 사용하여 객체를 탐지합니다.
        custDetect: 사용자 정의 YOLO 모델을 사용하여 객체를 탐지합니다.
        getOrgLabel: 일반 모델에 의해 탐지된 객체의 라벨을 반환합니다.
        getCustLabel: 사용자 정의 모델에 의해 탐지된 객체의 라벨을 반환합니다.
    """

    modelManager = ModelManager()
    orginNames = None  # 일반 모델의 라벨
    customNames = None  # 사용자 정의 모델의 라벨
    
    def __init__(self):
        """
        ObjectDetect 클래스를 초기화합니다.
        """
        origin = self.modelManager.orginModel
        custom = self.modelManager.customModel
        self.orginNames = self.origin.names
        self.customNames = self.custom.names
        
    def origin_detect(self, img):
        """일반 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            img (numpy.ndarray): 원본 이미지입니다.

        Returns:
            tuple: 바운딩 박스의 목록과 각 객체가 얼굴인지를 나타내는 목록을 포함하는 튜플입니다.
        """
        results = self.modelManager.orginModel.predict(img, verbose=False, show=False)  # 일반 모델로 결과 예측
        orgClss = results[0].boxes.cls.cpu().tolist()   # 탐지된 객체의 클래스 라벨 가져오기
        orgBoxes = results[0].boxes.xyxy.cpu().tolist() # 탐지된 객체의 좌표 가져오기
        boxesList = []  
        labelList = []
        
        if orgBoxes is not None:
            for box, cls in zip(orgBoxes, orgClss):
                boxesList.append(box) 
                labelList.append(self.orginNames[cls])
        return boxesList, labelList

    def custom_detect(self, frame):
        """사용자 정의 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            frame (numpy.ndarray): 원본 이미지입니다.

        Returns:
            list: 탐지된 객체의 바운딩 박스 목록입니다.
        """
        results2 = self.modelManager.customModel.predict(frame, verbose=False, show=False) # 사용자 정의 모델로 결과 예측
        custBoxes = results2[0].boxes.xyxy.cpu().tolist()   
        custClss = results2[0].boxes.cls.cpu().tolist()     
        boxesList = []
        labelList = []
        
        if custBoxes is not None:
            for box, cls in zip(custBoxes, custClss):
                boxesList.append(box)
                labelList.append(self.customNames[cls])
                
        return boxesList, labelList
    