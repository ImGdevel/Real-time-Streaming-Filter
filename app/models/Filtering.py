from .ObjectDetect import ObjectDetect
from .FaceFilter import *
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
        self.faceManager = FaceManager()
        self.stickerManager = StickerManager()
        self.pathManeger = PathManager()
        self.face_recog_frame = 0

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
        """return 값 results = {key:[[[box], confidence, label],]} 여기서 box는 x1, y1, w, h의 형식"""
        known_face_ids = []
        for name in self.current_filter_info.face_filter.keys():
            known_face_ids.append(name)
            results[name] = []

        origins = self.object.origin_detect(img, conf ,mag_ratio)  # 수정: results는 [[box], confidence, label]의 리스트 여기서의 box는 xywh의 값이므로 변환 필요
        for result in origins:  # 수정: isFace를 is_face로 변경                
            box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
            # cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]), (0,255,0), 2)
            # cv2.putText(img, "face"+str(result[1]), (box[0] + 5, box[1] - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
            face_encode = face_encoding_box(img, box)
            # cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0,255,0), 2)
            is_known = identify_known_face(known_face_ids, face_encode, self.pathManeger.load_known_faces_path())
            if is_known is not None: 
                results[int(is_known)].append(result)
            else:
                results[-1].append(result)
        return results
    
    def object_filter(self, img, results):
        """return 값 results = {key:[[box],],} 여기서 box는 xyxy의 형태"""
        customs = self.object.custom_detect(img)
        for result in customs:
            if result[2] in self.current_filter_info.object_filter:
                box = [result[0][0], result[0][1], result[0][0]+result[0][2], result[0][1]+result[0][3]] # xywh를 xyxy형태로 변환
                results[-2].append(box)
        return results
    

    def background_blur(self, img):
        mp_selfie_segmentation = mp.solutions.selfie_segmentation
        BG_COLOR = (200,200,200)

        with mp_selfie_segmentation.SelfieSegmentation(model_selection=1) as selfie_segmentation:
            # 이미지 처리 과정 (img는 입력 이미지로 가정)
            img.flags.writeable = False
            results = selfie_segmentation.process(img)
            img.flags.writeable = True

            # 세그멘테이션 마스크 생성
            condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.5

            # 배경을 흐리게 처리
            blurred_background = cv2.GaussianBlur(img, (55, 55), 0)

            # 경계를 부드럽게 만들기 위해 사람 영역 확장
            kernel = np.ones((10, 10), np.uint8)  # 작은 kernel 크기로 변경
            dilated_condition = cv2.dilate(condition.astype(np.uint8), kernel, iterations=2)  # 작은 iteration 값으로 변경

            # 흐린 배경과 원본 이미지를 조합하여 부드러운 경계 생성
            img = np.where(dilated_condition, img, blurred_background)
        return img

    def get_area_img(self, img, box):
        focus_img = img[box[1]:box[3], box[0]:box[2]]
        focus_img = np.ascontiguousarray(focus_img)
        return focus_img
    
    def is_dup(self, new, results):
        already = []
        for box in results.values():
            already.extend(box)
        
        for box in already:
            if len(box) > 0:
                x1, y1, x2, y2 = box[0][0], box[0][1], box[0][0]+box[0][2], box[0][1]+box[0][3]
                nx1, ny1, nx2, ny2 = new[0][0], new[0][1], new[0][0]+new[0][2], new[0][1]+new[0][3]

                
                intersection_x1 = max(x1, nx1)
                intersection_y1 = max(y1, ny1)
                intersection_x2 = min(x2, nx2)
                intersection_y2 = min(y2, ny2)

                intersection_width = max(0, intersection_x2 - intersection_x1)
                intersection_height = max(0, intersection_y2 - intersection_y1)
                intersection_area = intersection_height * intersection_width
                if intersection_area / (new[0][2]*new[0][3]) >= 0.7:
                    print("box:",box[0])
                    print("new:",new[0])
                    return True
 
        return False

    def filtering(self, img, is_video=True, focus_area=None):
        results = dict()
        results[-2] = []
        results[-1] = []

        if self.current_filter_info is None:
            return results
                
        temp_ratio = self.current_filter_info.imgsz_mag * 3 / 100 + 0.01 # 임시로 UI사용하려고 만든 todo 0.01은 0 되지 말라고 넣어놨는데 if로 했다가 이게 더 나은거같음
        conf = self.current_filter_info.predict_conf / 100
        #print(temp_ratio)
        
        results = self.face_filter(img, results, conf, temp_ratio)
        
        if focus_area is not None:
            focus_img = self.get_area_img(img, focus_area)
            temp = {-2:[], -1:[]}
            focus_result = self.face_filter(focus_img, temp, conf, temp_ratio)
            for key, value in focus_result.items():
                for box in value:
                    if len(box) > 0:
                        box[0][0] += focus_area[0]
                        box[0][1] += focus_area[1]
                        if not self.is_dup(box, results):
                            results[key].append(box)
        
        if is_video:
            if len(results) != 0:
                results = self.object.object_track(img, results)
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


        results = self.object_filter(img, results)
        results = self.filter_state_check(results)

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
        if face_id not in self.current_filter_info.face_filter.keys():
            return self.blur(img, boxesList)
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
        if (current_filter is None) | (current_filter == False) :
            self.current_filter_info = None
        else :
            self.current_filter_info = current_filter
            if "Human face" not in self.current_filter_info.object_filter:
                self.current_filter_info.object_filter.append("Human face")
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
            

