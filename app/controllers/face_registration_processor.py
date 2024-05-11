from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QPixmap, QImage
from controllers import PersonFaceSettingController
import cv2
import numpy as np

class FaceRegistrationProcessor(QThread):
    countChanged = Signal(int)
    addItem = Signal(QImage)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._is_canceled = False
        self.face_setting_processor = PersonFaceSettingController()
        self.ndarray_images = []
        self.current_person = None
        
    def setup(self, images: list[np.ndarray], person):
        """Initialize images and person."""
        self.ndarray_images = images
        self.current_person = person

    def run(self):
        try:
            if self.current_person.face_name is None:
                raise ValueError("Person's face name is not set.")
                
            for ndarray in self.ndarray_images:
                image = ndarray
                if self.face_setting_processor.add_person_encoding_by_name(self.current_person.face_name, image):
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    height, width, channel = image.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    self.addItem.emit(q_image)
                else:
                    print("Image registration failed")
        except ValueError as e:
            print("Image registration error:", e)
        finally:
            self.finished.emit()

    def cancel(self):
        """Cancel the registration process."""
        self._is_canceled = True
