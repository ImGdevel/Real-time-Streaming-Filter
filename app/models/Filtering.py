from models.ObjectDetect import ObjectDetect
from models.FaceFilter import *
import cv2

class Filtering:
    """
    A class for applying filtering techniques to images based on detected objects.
    
    Attributes:
        object (ObjectDetect): An instance of ObjectDetect class for object detection.
        
    Methods:
        __init__: Initializes the Filtering class with an ObjectDetect instance.
        filtering: Filters the image based on detected objects and optionally on faces.
        blur: Applies blurring to the regions of interest specified by boxesList.
    """
    
    def __init__(self):
        """
        Initializes the Filtering class.
        """
        self.object = ObjectDetect()
        
    def filtering(self, img, objects, except_people=['test']):
        """
        Filters the image based on detected objects and optionally on faces.

        Args:
            img (numpy.ndarray): Input image.
            objects (list): List of objects to detect.
            face (bool, optional): Whether to detect faces. Defaults to None.

        Returns:
            list: List of bounding boxes for detected objects.
        """

        results = []
        boxesList, labelList = self.object.orgDetect(img)  # Corrected: unpacking the tuple
        for box, label in zip(boxesList, labelList):  # Corrected: renamed isFace to is_face

            if label == "Human face":
                print("If it's a Human face")
                face_encode = face_encoding_box(img, box)

                if is_known_person(except_people, face_encode):
                    continue
                else :
                    results.append(box)
                    continue

            if objects[label] == 1:
                results.append(box)

        custList = []
        custList, labelList = self.object.custDetect(img)
        for obj, label in zip(custList, labelList):
            if objects[label] == 1:
                results.append(obj)
            
        return results
    
    def blur(self, blurRatio, img, boxesList):
        """
        Applies blurring to the regions of interest specified by boxesList.

        Args:
            blurRatio (int): Blurring ratio.
            img (numpy.ndarray): Input image.
            boxesList (list): List of bounding boxes for the regions of interest in YOLO format (box[0], box[1], box[2], box[3]).

        Returns:
            img (numpy.ndarray): Modified image with blurring applied to specified regions.
        """
        for box in boxesList:

            
            # 정수로 변환
            roi = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]

            # ROI에 blur 적용
            blurred_roi = cv2.blur(roi, (blurRatio, blurRatio))
            
            # blur 적용된 ROI를 원본 이미지에 다시 넣어줌
            img[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blurred_roi
            
        return img