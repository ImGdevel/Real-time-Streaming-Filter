from .ObjectDetect import ObjectDetect
from .FaceFilter import *
from .ModelManager import ModelManager
from .replace_manager import ReplaceManager
from .face_manager import FaceManager
from .filter_info import Filter
from .path_manager import PathManager
import cv2
import numpy as np

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
        self.faceManager = FaceManager()
        self.replaceManager = ReplaceManager()
        self.pathManeger = PathManager()
        self.face_recog_frame = 0

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
        if filter_info is None:
            filter_info = Filter("test")
        if filter_info.face_filter_on:
            if "Human face" not in filter_info.object_filter:
                filter_info.object_filter.append("Human face")
        self.object.set_filter_classes(filter_info.object_filter)
        results = []
        known_faces_id = []
        for name in filter_info.face_filter:
            known_faces_id.append(self.faceManager.get_person_face_id(name))

        origins = self.object.origin_detect(img)  # 수정: results는 [[box], confidence, label]의 리스트 여기서의 box는 xywh의 값이므로 변환 필요
        for result in origins:  # 수정: isFace를 is_face로 변경                
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            if filter_info.face_filter_on is True:
                if result[2] == "Human face":
                    # print("사람 얼굴일 경우")
                    face_encode = face_encoding_box(img, box)
                    if is_known_person(known_faces_id, face_encode):
                        continue
                    else :
                        results.append(box)
                        continue
            if result[2] in filter_info.object_filter:
                results.append(box)

        customs = self.object.custom_detect(img)
        for result in customs:
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            if result[2] in filter_info.object_filter:
                results.append(box)
            
        return results
    
    def video_filtering(self, img, filter_info = Filter("test")):
        if filter_info is None:
            filter_info = Filter("test")
        if filter_info.face_filter_on:
            if "Human face" not in filter_info.object_filter:
                filter_info.object_filter.append("Human face")
        self.object.set_filter_classes(filter_info.object_filter)
        results = []
        known_faces_id = []
        known_face_boxes = []
        for name in filter_info.face_filter:
            known_faces_id.append(self.faceManager.get_person_face_id(name))

        origins = self.object.origin_detect(img)  # 수정: results는 [[box], confidence, label]의 리스트 여기서의 box는 xywh의 값이므로 변환 필요
        for result in origins:  # 수정: isFace를 is_face로 변경                
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            # print(result[2])
            if filter_info.face_filter_on is True:
                if result[2] == "Human face":
                    # print("사람 얼굴일 경우")
                    self.face_recog_frame += 1
                    if self.face_recog_frame == 1:
                        face_encode = face_encoding_box(img, box)

                        if is_known_person(known_faces_id, face_encode, self.pathManeger.known_faces_path()):
                            known_face_boxes.append(result[0])
                        results.append(result)
                        continue
                    if self.face_recog_frame == 10:
                        self.face_recog_frame = 0
                    
            if result[2] in filter_info.object_filter:
                results.append(result)

        customs = self.object.custom_detect(img)
        for result in customs:
            if result[2] in filter_info.object_filter:
                results.append(result)
        
        results = self.object.object_track(img, results, known_face_boxes)


        boxes = []
        for result in results:
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            boxes.append(box)
        return boxes
    
    def blur(self,img, boxesList, blurRatio = 50):
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

    def elliptical_blur(self, img, boxesList):
        for box in boxesList:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            if x1 > 640 or y1 > 480 or x2 < 0 or y2 < 0:
                return
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            obj = img[y1:y2, x1:x2]

            # Calculate blur region size
            blur_w = int((x2 - x1) * 0.5)  # 가로 길이의 절반
            blur_h = int((y2 - y1) * 0.5)  # 세로 길이의 절반

            if blur_w <= 0 or blur_h <= 0:
                return
            # Apply blur in elliptical shape
            blur_obj = cv2.blur(obj, (blur_w, blur_h))

            # Create mask for elliptical shape
            mask = np.zeros_like(obj)   
            center = (int((x2 - x1) / 2), int((y2 - y1) / 2))
            axes = (int((x2 - x1) / 2), int((y2 - y1) / 2))
            cv2.ellipse(mask, center, axes, 0, 0, 360, (255, 255, 255), -1)

            # Combine blurred object with mask to create elliptical blur effect
            elliptical_blur = cv2.bitwise_and(blur_obj, mask)
            obj = cv2.bitwise_and(obj, cv2.bitwise_not(mask))
            obj = cv2.add(obj, elliptical_blur)

            # Replace original object region with blurred object
            img[y1:y2, x1:x2] = obj
        return img
    
    def replace_face_img(self, img, boxesList, replace_img_id):
        # for box in boxesList:
        #     x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        #     w = x2-x1
        #     h = y2-y1

        #     replace_img = self.replaceManager.load_img_
