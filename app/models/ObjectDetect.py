from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator, colors
import cv2

class ObjectDetect:
    """
    A class for object detection using YOLO models.

    Attributes:
        origin (YOLO): YOLO model for general object detection.
        custom (YOLO): YOLO model for detecting custom objects.
        orgNames (list): Labels for objects detected by the general model.
        custNames (list): Labels for objects detected by the custom model.

    Methods:
        __init__: Initializes the ObjectDetect class with YOLO models and their labels.
        originDetect: Detects objects using the general YOLO model.
        custDetect: Detects custom objects using the custom YOLO model.
        getOrgLabel: Returns the labels for objects detected by the general model.
        getCustLabel: Returns the labels for objects detected by the custom model.
    """

    origin = YOLO("models/yolov8n-oiv7.pt")   # General object detection model
    custom = YOLO("models/bad.pt")   # Custom object detection model
    orgNames = None  # Labels for the general model
    custNames = None  # Labels for the custom model
    
    def __init__(self):
        """
        Initializes the ObjectDetect class.
        """
        self.orgNames = self.origin.names
        self.custNames = self.custom.names
        
    def orgDetect(self, img):
        """Detects objects using the general YOLO model.

        Args:
            img (numpy.ndarray): Source image.

        Returns:
            tuple: A tuple containing lists of bounding boxes and a list indicating whether each object is a human face.
        """
        results = self.origin.predict(img, show=False)  # Predict results using the general model
        orgClss = results[0].boxes.cls.cpu().tolist()   # Get class labels of detected objects
        orgBoxes = results[0].boxes.xyxy.cpu().tolist() # Get coordinates of detected objects
        annotator = Annotator(img, line_width=2, example=self.orgNames)
        boxesList = []  
        isFace = []
        
        if orgBoxes is not None:
            for box, cls in zip(orgBoxes, orgClss):
                annotator.box_label(box, color=colors(int(cls), True), label=self.orgNames[int(cls)])
                if self.orgNames[cls] == "Human face":
                    isFace.append(True)
                else:
                    isFace.append(False)
                boxesList.append(box) 
        return boxesList, isFace

    def custDetect(self, frame):
        """Detects custom objects using the custom YOLO model.

        Args:
            frame (numpy.ndarray): Source image.

        Returns:
            list: List of bounding boxes for detected objects.
        """
        results2 = self.custom.predict(frame, show=False) # Predict results using the custom model
        custBoxes = results2[0].boxes.xyxy.cpu().tolist()   
        custClss = results2[0].boxes.cls.cpu().tolist()     
        annotator = Annotator(frame, line_width=2, example=self.custNames)
        boxesList = []  
        
        if custBoxes is not None:
            for box, cls in zip(custBoxes, custClss):
                annotator.box_label(box, color=colors(int(cls), True), label=self.custNames[int(cls)])
                boxesList.append(box)
                
        return boxesList
    
    def getOrgLabel(self):
        """
        Returns the labels for objects detected by the general model.

        Returns:
            list: Labels for objects detected by the general model.
        """
        return self.orgNames
    
    def getCustLabel(self):
        """
        Returns the labels for objects detected by the custom model.

        Returns:
            list: Labels for objects detected by the custom model.
        """
        return self.custNames