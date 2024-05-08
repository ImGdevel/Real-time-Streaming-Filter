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
        """인식할 객체 목록들을 설정한다."""
        for key, value in self.orginNames.items():
            if value in filter_classes:
                self.originFilterClasses.append(key)
        for key, value in self.customNames.items():
            if value in filter_classes:
                self.customFilterClasses.append(key)

    def set_known_faces(self, face_list: list):
        self.sticker_id = dict()
        for face in face_list:
            self.sticker_id[face] = []
        #print("sticker_id: ", self.sticker_id)

    def detect(self, img, filter_classes, model, names):
        """
        객체인식 결과를 반환한다.
        img: 객체 인식이 필요한 이미지
        filter_classes: 인식할 객체 목록
        model: 객체 인식 모델
        names: 객체 이름 목록

        return: [[box], 신뢰도, 객체 이름]의 리스트를 반환한다.
        """
        results = []
        
        if not filter_classes:
            return results
        detection = model.predict(img, verbose=False, classes=filter_classes, show=False)[0]  # 일반 모델로 결과 예측

        for data in detection.boxes.data.tolist():
            confidence = float(data[4])
            if confidence < self.CONFIDENCE_THRESHOLD:
                continue
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = names[int(data[5])]
            results.append([[xmin, ymin, xmax-xmin, ymax-ymin], confidence, label])
        return results 
    
    def origin_detect(self, img):
        """일반 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            img (numpy.ndarray): 원본 이미지입니다.

        Returns:
            tuple: 바운딩 박스의 목록과 각 객체가 얼굴인지를 나타내는 목록을 포함하는 튜플입니다.
        """
        return self.detect(img, self.originFilterClasses, self.modelManager.orginModel, self.orginNames)

    def custom_detect(self, img):
        """사용자 정의 YOLO 모델을 사용하여 객체를 탐지합니다.

        Args:
            frame (numpy.ndarray): 원본 이미지입니다.

        Returns:
            list: 탐지된 객체의 바운딩 박스 목록입니다.
        """
        return self.detect(img, self.customFilterClasses, self.modelManager.customModel, self.customNames)
    
    def object_track(self, img, results):
        """주어진 이미지와 좌표에 대한 객체 추적 결과를 반환한다."""
        detections = []
        for value in results.values():
            detections.extend(value)
        tracks = self.modelManager.tracker.update_tracks(detections, frame=img)
        last_results = dict()
        last_results[-1] = []
        for track in tracks:
            float_box = track.to_ltrb(orig=True).tolist()
            int_box = [int(float_box[0]), int(float_box[1]), int(float_box[2]), int(float_box[3])]
            if not track.is_confirmed():
                last_results[-1].append(int_box)
                continue
            box = track.to_ltwh(orig=True).tolist()
            for face in results.keys():
                if face != -1:
                    if len(results[face]) != 0:
                        if box == results[face][0][0]:
                            self.sticker_id[face] = track.track_id

            is_sticker = False
            for sticker in self.sticker_id.keys():
                if track.track_id == self.sticker_id[sticker]:
                    last_results[sticker] = [int_box]
                    is_sticker = True
                    break
            if is_sticker == False:
                last_results[-1].append(int_box)

        return last_results
    
    def init_exclude_id(self):
        """저장된 track_id를 초기화한다"""
        self.exclude_id = []