from PySide6.QtCore import Signal, QThread
from PySide6.QtGui import QPixmap
from controllers import PersonFaceSettingController

class FaceRegistrationProcessor(QThread):
    countChanged = Signal(int)
    addItem = Signal(QPixmap)
    finished = Signal()

    def __init__(self):
        super().__init__()
        self._is_canceled = False
        self.face_setting_processor = PersonFaceSettingController()
        self.pixmap_images = []
        self.current_person = None
        
    def setup(self, images: list[QPixmap], person):
        """Initialize images and person."""
        self.pixmap_images = images
        self.current_person = person

    def run(self):
        try:
            if self.current_person.face_name is None:
                raise ValueError("Person's face name is not set.")
                
            for pixmap in self.pixmap_images:
                image = pixmap.toImage()
                if self.face_setting_processor.add_person_encoding_by_name(self.current_person.face_name, image):
                    self.addItem.emit(pixmap)
                else:
                    print("Image registration failed")
        except ValueError as e:
            print("Image registration error:", e)
        finally:
            self.finished.emit()

    def cancel(self):
        """Cancel the registration process."""
        self._is_canceled = True
