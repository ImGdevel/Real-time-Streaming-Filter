from .ObjectDetect import ObjectDetect
from .FaceFilter import *
from .ModelManager import ModelManager
from .sticker_manager import StickerManager
from .face_manager import FaceManager
from .filter_info import Filter
from .path_manager import PathManager
import cv2
import numpy as np
import mediapipe as mp

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
        self.stickerManager = StickerManager()
        self.pathManeger = PathManager()
        self.face_recog_frame = 0

        known_faces = None

        self.current_filter_info = None
        self.change_filter_info = None
        self.init_id = False
        self.filter_change = False

    def face_capture(self, img):
        boxList = self.object.face_detect(img)
        for box in boxList:
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (255, 255, 255), 2)
        return img


    def face_filter(self, img, results, conf = 10 ,mag_ratio = 1):
        known_face_ids = []
        for name in self.current_filter_info.face_filter.keys():
            known_face_ids.append(name)
            results[name] = []

        origins = self.object.origin_detect(img, conf ,mag_ratio)  # 수정: results는 [[box], confidence, label]의 리스트 여기서의 box는 xywh의 값이므로 변환 필요
        for result in origins:  # 수정: isFace를 is_face로 변경                
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), (0,255,0), 2)
            cv2.putText(img, "face"+str(result[1]), (box[0] + 5, box[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            if result[2] == "Human face":
                face_encode = face_encoding_box(img, box)
                # cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0,255,0), 2)
                is_known = identify_known_face(known_face_ids, face_encode, self.pathManeger.load_known_faces_path())
                if is_known is not None: 
                    results[int(is_known)].append(result)
                else:
                    results[-1].append(result)
            else:
                results[-3].append(result)
        return results
    
    def object_filter(self, img, results):
        customs = self.object.custom_detect(img)
        for result in customs:
            if result[2] in self.current_filter_info.object_filter:
                box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
                results[-2].append(box)
        return results
    
    def remove_high_overlap_boxes_within_list(self, boxes, threshold=0.9):
        def calculate_area(box):
            x1, y1, x2, y2 = box
            return (x2-x1) * (y2-y1)

        def calculate_intersection_area(box1, box2):
            x1_1, y1_1, x2_1, y2_1 = box1
            x1_2, y1_2, x2_2, y2_2 = box2

            intersection_x1 = max(x1_1, x1_2)
            intersection_y1 = max(y1_1, y1_2)
            intersection_x2 = min(x2_1, x2_2)
            intersection_y2 = min(y2_1, y2_2)

            intersection_width = max(0, intersection_x2 - intersection_x1)
            intersection_height = max(0, intersection_y2 - intersection_y1)

            return intersection_width * intersection_height

        filtered_boxes = boxes.copy()

        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                box_a = boxes[i]
                box_b = boxes[j]
                intersection_area = calculate_intersection_area(box_a, box_b)
                area_a = calculate_area(box_a)
                area_b = calculate_area(box_b)

                if intersection_area / area_a >= threshold or intersection_area / area_b >= threshold:
                    if box_b in filtered_boxes:
                        filtered_boxes.remove(box_b)

        return filtered_boxes


    def fully_overlapping_boxes(self, a_boxes, b_boxes):
        fully_overlapping = []

        for box_a in a_boxes:
            x1_a, y1_a, x2_a, y2_a = box_a

            for box_b in b_boxes:
                x1_b, y1_b, x2_b, y2_b = box_b

                # box_a가 box_b 안에 완전히 포함되는지 확인
                if (x1_a >= x1_b and y1_a >= y1_b and x2_a <= x2_b and y2_a <= y2_b):
                    fully_overlapping.append(box_b)
                    break

        return fully_overlapping

    def blur_background(self, image, box_list, blur_kernel_size=(55, 55)):
        blurred_image = image.copy()
        persons = []
        faces = []
        temp = []
        for key, box in box_list.items():
            if len(box) > 0:
                if key == -3:
                    persons.extend(box)
                elif key >= -1:
                    faces.extend(box)
        if len(persons) > 0 and len(faces) > 0:
            persons = self.remove_high_overlap_boxes_within_list(persons)
            temp = self.fully_overlapping_boxes(faces, persons)
        elif len(faces) == 0:
            temp = []

        if len(temp) == 0:
            # temp가 비었을 경우 전체 이미지를 블러 처리
            image = cv2.GaussianBlur(image, blur_kernel_size, 0)
        # 박스 리스트 순회
        for box in temp:
            x1, y1, x2, y2 = box[0], box[1], box[0]+box[2], box[1]+box[3]  # 박스의 좌표 (x1, y1): 좌상단, (x2, y2): 우하단

            # 박스에 해당하는 부분은 스킵
            blurred_image[y1:y2, x1:x2] = image[y1:y2, x1:x2]

        # 전체 이미지에서 박스에 해당하지 않는 부분에만 가우시안 블러 적용
        mask = np.ones_like(image, dtype=np.uint8) * 255
        for box in temp:
            x1, y1, x2, y2 = box[0], box[1], box[0]+box[2], box[1]+box[3]  # 박스의 좌표 (x1, y1): 좌상단, (x2, y2): 우하단
            mask[y1:y2, x1:x2] = 0  # 박스에 해당하는 부분은 마스크에서 0으로 설정

        blurred_background = cv2.GaussianBlur(image, blur_kernel_size, 0)
        blurred_image = np.where(mask == 255, blurred_background, blurred_image)

        return blurred_image
    
    def background_blur(self, img):
        mp_drawing = mp.solutions.drawing_utils
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        BG_COLOR = (255, 255, 255)
        with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            # 이미지 처리 과정 (img는 입력 이미지로 가정)
            img.flags.writeable = False
            results = selfie_segmentation.process(img)
            img.flags.writeable = True

            # 세그멘테이션 마스크 생성
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1

            # 배경을 흐리게 처리
            blurred_background = cv2.GaussianBlur(img, (55, 55), 0)

            # 경계를 부드럽게 만들기 위해 사람 영역 확장
            kernel = np.ones((15, 15), np.uint8)
            dilated_condition = cv2.dilate(condition.astype(np.uint8), kernel, iterations=3)

            # 흐린 배경과 원본 이미지를 조합하여 부드러운 경계 생성
            img = np.where(dilated_condition, img, blurred_background)
        return img

    def filtering(self, img, is_video=True):
        if self.current_filter_info is None:
            return dict()
                
        results = dict()
        results[-3] = []
        results[-2] = []
        results[-1] = []
        temp_ratio = self.current_filter_info.imgsz_mag * 3 / 100 + 0.01 # 임시로 UI사용하려고 만든 todo 0.01은 0 되지 말라고 넣어놨는데 if로 했다가 이게 더 나은거같음
        conf = self.current_filter_info.predict_conf / 100
        #print(temp_ratio)
        
        results = self.face_filter(img, results, conf, temp_ratio)
        
        if is_video:
            if len(results) != 0:
                temp = []
                for box in results[-3]:
                    tb = [box[0][0], box[0][1], box[0][0]+box[0][2], box[0][1]+box[0][3]]
                    temp.append(tb)
                del results[-3]
                results = self.object.object_track(img, results)
                results[-3] = temp
            if self.init_id is True:
                self.object.init_exclude_id()
                self.init_id = False
        else:
            for key, result in results.items():
                boxes = []
                for value in result:
                    if len(value) != 0:
                        box = [value[0][0], value[0][1], value[0][0]+value[0][2], value[0][1]+value[0][3]]
                        boxes.append(box)
                results[key] = boxes

        results = self.filter_state_check(results)

        results = self.object_filter(img, results)
        # print("results:",results)
        return results
    
    def blur(self, img, boxesList):
        if self.current_filter_info is None:
            return img
        if self.current_filter_info.mosaic_blur_shape == "rect":
            return self.square_blur(img, boxesList)
        else:
            return self.elliptical_blur(img, boxesList)


    def square_blur(self,img, boxesList):
        """
        boxesList에 지정된 관심 영역에 블러를 적용합니다.

        Args:
            blurRatio (int): 블러 비율입니다.
            img (numpy.ndarray): 입력 이미지입니다.
            boxesList (list): YOLO 형식의 바운딩 박스 목록입니다 (box[0], box[1], box[2], box[3]).

        Returns:
            img (numpy.ndarray): 지정된 영역에 블러가 적용된 수정된 이미지입니다.
        """
        if self.current_filter_info is None:
            return img
        blurRatio = self.current_filter_info.mosaic_blur_strength
        for box in boxesList:

            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            # 정수로 변환
            roi = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

            # Calculate blur region size
            blur_w = int((x2 - x1)*blurRatio/150) 
            blur_h = int((y2 - y1)*blurRatio/150)  
            if blur_w <= 0 or blur_h <= 0:
                return img
            # ROI에 blur 적용
            blurred_roi = cv2.blur(roi, (blur_w, blur_h))
            
            # blur 적용된 ROI를 원본 이미지에 다시 넣어줌
            img[y1:y2, x1:x2] = blurred_roi
            
        return img

    def elliptical_blur(self, img, boxesList):
        if self.current_filter_info is None:
            return img
        blurRatio = self.current_filter_info.mosaic_blur_strength
        for box in boxesList:
            if len(box) == 0:
                continue
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            obj = img[y1:y2, x1:x2]

            # Calculate blur region size
            # Calculate blur region size
            blur_w = int((x2 - x1)*blurRatio/150) 
            blur_h = int((y2 - y1)*blurRatio/150)  

            # ROI에 blur 적용

            if blur_w <= 0 or blur_h <= 0:
                return img
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
    
    def face_sticker(self, img, boxesList, face_id):
        if self.current_filter_info.face_filter[face_id] == -1:
            return img
        for box in boxesList:
            x1, y1, x2, y2 = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            w = x2 - x1
            h = y2 - y1

            x_center = int((x1 + x2) / 2)
            y_center = int((y1 + y2) / 2)

            replace_img_id = self.current_filter_info.face_filter[face_id]
            replace_img = self.stickerManager.load_img_to_id(replace_img_id)
            r_h, r_w = replace_img.shape[:2]

            if w > h:
                aspect_ratio = w / r_w
            else:
                aspect_ratio = h / r_h

            n_w = int(r_w * aspect_ratio)
            n_h = int(r_h * aspect_ratio)

            replace_img_resized = cv2.resize(replace_img, (n_w, n_h))
            resize_x1 = x_center - int(n_w / 2)
            resize_x2 = x_center + int(n_w / 2)
            resize_y1 = y_center - int(n_h / 2)
            resize_y2 = y_center + int(n_h / 2)

            # 경계 검사 후 보정
            if resize_x1 < 0:
                resize_x1 = 0
            if resize_x2 > img.shape[1]:
                resize_x2 = img.shape[1]

            if resize_y1 < 0:
                resize_y1 = 0
            if resize_y2 > img.shape[0]:
                resize_y2 = img.shape[0]

            for c in range(0, 3):
                roi = img[resize_y1:resize_y2, resize_x1:resize_x2, c]
                replace_img_resized_resized = cv2.resize(replace_img_resized, (roi.shape[1], roi.shape[0]))
                img[resize_y1:resize_y2, resize_x1:resize_x2, c] = roi * (
                        1.0 - replace_img_resized_resized[:, :, 3] / 255.0) + replace_img_resized_resized[:, :, c] * (
                                                                                replace_img_resized_resized[:, :, 3] / 255.0)

        return img
    
    def set_filter(self, current_filter:Filter = None):
        """변경될 필터 정보를 전달하고 필터를 변경해야 하는 상태라고 저장한다"""
        if self.current_filter_info is None:
            self.change_filter(current_filter)
            return
        self.change_filter_info = current_filter
        self.filter_change = True
        self.tracking_id_init()

    def change_filter(self, current_filter:Filter = None):
        """필터를 변경한다"""
        if current_filter is None :
            self.current_filter_info = None
        else :
            self.current_filter_info = current_filter
            if self.current_filter_info.face_filter_on:
                if "Human face" not in self.current_filter_info.object_filter:
                    self.current_filter_info.object_filter.append("Human face")
                if "Person" not in self.current_filter_info.object_filter:
                    self.current_filter_info.object_filter.append("Person")
                if "Woman" not in self.current_filter_info.object_filter:
                    self.current_filter_info.object_filter.append("Woman")
                if "Man" not in self.current_filter_info.object_filter:
                    self.current_filter_info.object_filter.append("Man")
            self.object.set_filter_classes(self.current_filter_info.object_filter)
            self.object.set_known_faces(current_filter.face_filter.keys())

    def filter_state_check(self, results):
        """filter가 변경됐는지 확인하고 변경사항을 적용한다."""
        temp = results
        if self.filter_change is True:
            self.change_filter(self.change_filter_info)
            self.change_filter_info = None
            self.filter_change = False
            temp = {}
            temp[-3] = results[-3]
            temp[-2] = results[-2]
            temp[-1] = results[-1]
            faces = []
            for key, value in results.items():
                if key > -1:
                    faces.extend(value)
            temp[-1].extend(value)
        return temp

    def tracking_id_init(self):
        """저장된 track_id 정보를 초기화한다."""
        self.init_id = True
            

