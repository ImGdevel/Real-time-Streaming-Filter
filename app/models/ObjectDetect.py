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
        self.sticker_id = dict()
        self.CONFIDENCE_THRESHOLD = 0.2
    
    def set_filter_classes(self, filter_classes:list):
        for key, value in self.orginNames.items():
            if value in filter_classes:
                self.originFilterClasses.append(key)
        for key, value in self.customNames.items():
            if value in filter_classes:
                self.customFilterClasses.append(key)

    def set_known_faces(self, face_list: list):
        for face in face_list:
            self.sticker_id[face] = []
        print("sticker_id: ", self.sticker_id)

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
    
    def object_track(self, img, results):
        detections = []
        for value in results.values():
            detections.extend(value)
        print("detections: ", detections)
        tracks = self.modelManager.tracker.update_tracks(detections, frame=img)
        last_results = dict()
        last_results[-1] = []
        for track in tracks:
            xy_box = track.to_ltrb(orig=True).tolist()
            if not track.is_confirmed():
                last_results[-1].append(xy_box)
                continue
            box = track.to_ltwh(orig=True).tolist()
            for face in results.keys():
                if face != -1:
                    if len(results[face]) != 0:
                        print("box:",box)
                        print("results[face][0]:",results[face][0])
                        if box == results[face][0][0]:
                            self.sticker_id[face] = track.track_id

            is_sticker = False
            print("sticker_id:",self.sticker_id)
            print()
            for sticker in self.sticker_id.keys():
                if track.track_id == self.sticker_id[sticker]:
                    last_results[sticker] = [xy_box]
                    is_sticker = True
                    break
            if is_sticker == False:
                last_results[-1].append(xy_box)

        return last_results
    
    def init_exclude_id(self):
        self.exclude_id = []