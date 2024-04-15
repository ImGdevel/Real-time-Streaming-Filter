from models.ObjectDetect import ObjectDetect
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
        
    def filtering(self, img, objects, face=None):
        """
        Filters the image based on detected objects and optionally on faces.

        Args:
            img (numpy.ndarray): Input image.
            objects (list): List of objects to detect.
            face (bool, optional): Whether to detect faces. Defaults to None.

        Returns:
            list: List of bounding boxes for detected objects.
        """
        boxesList = []
        # boxesList, isFace = self.object.orgDetect(img)  # Corrected: unpacking the tuple
        # for box, is_face in zip(boxesList, isFace):  # Corrected: renamed isFace to is_face
        #     if is_face == True:
        #         # If it's a human face
        #         pass
        #     boxesList.append(box)
            
        custList = self.object.custDetect(img)
        for obj in custList:
            boxesList.append(obj)
            
        return boxesList
    
    def blur(self, blurRatio, img, boxesList):
        """
        Applies blurring to the regions of interest specified by boxesList.

        Args:
            blurRatio (int): Blurring ratio.
            img (numpy.ndarray): Input image.
            boxesList (list): List of bounding boxes for the regions of interest.

        Returns:
            None
        """
        for box in boxesList:
            temp = img[int(box[1]):int(box[3]), int(box[0]):int(box[2])]
            blur_obj = cv2.blur(temp, (blurRatio, blurRatio))
            img[int(box[1]):int(box[3]), int(box[0]):int(box[2])] = blur_obj