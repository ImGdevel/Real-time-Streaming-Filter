from ultralytics import YOLO
from dataclasses import dataclass, field
from deep_sort_realtime.deepsort_tracker import DeepSort


class ModelManager:
    '''
    ObjectFilter클래스가 객체 인식에 사용하는 범용 모델과 사용자정의 모델이 들어있다.
    '''
    _instance = None
    orginModel: YOLO
    customModel: YOLO
    tracker: DeepSort

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.orginModel = YOLO("models/yolov8m-oiv7.pt")
            cls.customModel = YOLO("models/bad.pt")
            cls.tracker = DeepSort(max_age=10)
        return cls._instance
    
    def get_label(self):
        label = list(self.orginModel.names.values())
        custom = list(self.customModel.names.values())
        for c in custom:
            if c not in label:
                label.append(c)

        return label
     