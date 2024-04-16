from models.ObjectDetect import ObjectDetect
from models.FaceFilter import *
from models.ModelManager import ModelManager
from models.filter_info import Filter
import cv2

class Filtering:
    """
    객체를 감지하여 이미지에 필터링 기법을 적용하는 클래스입니다.
    
    속성:
        object (ObjectDetect): 객체 감지를 위한 ObjectDetect 클래스의 인스턴스입니다.
        
    메서드:
        __init__: ObjectDetect 인스턴스를 사용하여 Filtering 클래스를 초기화합니다.
        filtering: 감지된 객체와 선택적으로 얼굴을 기반으로 이미지를 필터링합니다.
        blur: boxesList에 지정된 관심 영역에 블러를 적용합니다.
    """
    
    def __init__(self):
        """
        Filtering 클래스를 초기화합니다.
        """
        self.object = ObjectDetect()
        self.modelManager = ModelManager()
        
    def filtering(self, img, filter_info = Filter("test")):
        """
        감지된 객체와 선택적으로 얼굴을 기반으로 이미지를 필터링합니다.

        Args:
            img (numpy.ndarray): 입력 이미지입니다.
            objects (list): 감지할 객체의 목록입니다.
            face (bool, optional): 얼굴을 감지할지 여부입니다. 기본값은 None입니다.

        Returns:
            list: 감지된 객체의 바운딩 박스 목록입니다.
        """

        # results = []
        # boxesList, labelList = self.object.origin_detect(img)  # 수정: 튜플 언패킹
        # for box, label in zip(boxesList, labelList):  # 수정: isFace를 is_face로 변경
        #     if filter_info.face_filter_on is True:   
        #         if label == "Human face":
        #             print("사람 얼굴일 경우")
        #             face_encode = face_encoding_box(img, box)

        #             if is_known_person(filter_info.face_filter, face_encode):
        #                 continue
        #             else :
        #                 results.append(box)
        #                 continue    
        #     if label in filter_info.object_filter:
        #         results.append(box)

        # custList = []
        # custList, labelList = self.object.custom_detect(img)
        # for obj, label in zip(custList, labelList):
        #     if label in filter_info.object_filter:
        #         results.append(obj)
            
        # return results
    
    def blur(self, blurRatio, img, boxesList):
        """
        boxesList에 지정된 관심 영역에 블러를 적용합니다.

        Args:
            blurRatio (int): 블러 비율입니다.
            img (numpy.ndarray): 입력 이미지입니다.
            boxesList (list): YOLO 형식의 바운딩 박스 목록입니다 (box[0], box[1], box[2], box[3]).

        Returns:
            img (numpy.ndarray): 지정된 영역에 블러가 적용된 수정된 이미지입니다.
        """
        for box in boxesList:

            
            # 정수로 변환
            roi = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

            # ROI에 blur 적용
            blurred_roi = cv2.blur(roi, (blurRatio, blurRatio))
            
            # blur 적용된 ROI를 원본 이미지에 다시 넣어줌
            img[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blurred_roi
            
        return img
