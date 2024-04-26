from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
from .ModelManager import ModelManager
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
        self.orginNames = origin.names
        self.customNames = custom.names
        self.originFilterClasses = []
        self.customFilterClasses = []    
        self.exclude_id = []
        self.CONFIDENCE_THRESHOLD = 0.4
    
    def set_filter_classes(self, filter_classes:list):
        for key, value in self.orginNames.items():
            if value in filter_classes:
                self.originFilterClasses.append(key)
        for key, value in self.customNames.items():
            if value in filter_classes:
                self.customFilterClasses.append(key)

    def origin_detect(self, img):
        """일반 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            img (numpy.ndarray): 원본 이미지입니다.

        Returns:
            tuple: 바운딩 박스의 목록과 각 객체가 얼굴인지를 나타내는 목록을 포함하는 튜플입니다.
        """
        results = []
        
        if not self.originFilterClasses:
            return results
        detection = self.modelManager.orginModel.predict(img, verbose=False, classes=self.originFilterClasses, show=False)[0]  # 일반 모델로 결과 예측

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])
            if confidence < self.CONFIDENCE_THRESHOLD:
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = self.orginNames[int(data[5])]
            results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])

        return results 

    def custom_detect(self, img):
        """사용자 정의 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            frame (numpy.ndarray): 원본 이미지입니다.

        Returns:
            list: 탐지된 객체의 바운딩 박스 목록입니다.
        """
        results = []
        
        if not self.originFilterClasses:
            return results
        detection = self.modelManager.customModel.predict(img, verbose=False, classes=self.customFilterClasses, show=False)[0]  # 일반 모델로 결과 예측

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])
            if confidence < self.CONFIDENCE_THRESHOLD:
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = self.customNames[int(data[5])]
            results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])

        return results 
    
    def object_track(self, img, results, known_faces):
        tracks = self.modelManager.tracker.update_tracks(results, frame=img)
        last_results = []
        for track, result in zip(tracks,results):
            if not track.is_confirmed():
                continue

            track_id = track.track_id
            if result[0] in known_faces:
                if track_id not in self.exclude_id:
                    self.exclude_id.append(track_id)
            if track_id not in self.exclude_id:
                last_results.append(result)

        return last_results
    
    def init_exclude_id(self):
        self.exclude_id = []