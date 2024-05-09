from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication, QThread
from PySide6.QtGui import QPixmap, QIcon
from controllers import PersonFaceSettingController

class FaceRegistrationProcessor(QThread):
    countChanged = Signal(int)
    addItem = Signal(str)
    finished = Signal(list)

    def __init__(self):
        super().__init__()
        self._is_canceled = False
        self.face_setting_processor = PersonFaceSettingController()

    def setup(self, image_files, person):
        self.image_files = image_files
        self.current_person = person

    def run(self):
        failed_registration_images = []
        try:
            for idx, file_path in enumerate(self.image_files):
                if not self.current_person.face_name is None:
                    if self.face_setting_processor.add_person_encoding_by_name(self.current_person.face_name, file_path):  # 인코딩 하는 로직 인코딩이 성공하면 True / 실패하면 False
                        self.addItem.emit(file_path)
                    else:
                        print(f"이미지 등록 실패: {file_path}")
                        failed_registration_images.append(file_path)
        except Exception as e:
            print("이미지 등록 오류: ", e)
            
        finally:
            self.finished.emit(failed_registration_images)

    def cancel(self):
        self._is_canceled = True

