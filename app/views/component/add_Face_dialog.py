from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from controllers import PersonFaceSettingController
from .list_widget import AvailableFacesListWidget

class AddFaceDialog(QDialog):
    added_face = pyqtSignal(str)  # 얼굴 추가 시그널 선언
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.face_setting_processor = PersonFaceSettingController()
        self._initUI()

    def _initUI(self):
        """다이얼로그 UI 초기화 메서드"""
        self.setWindowTitle("Add Face")
        self.setFixedSize(600, 500)

        main_layout = QHBoxLayout()

        scroll_area = self._setup_scroll_area()
        face_registration_layout = self._setup_face_registration_layout()

        main_layout.addLayout(scroll_area)
        main_layout.addLayout(face_registration_layout)

        self.setLayout(main_layout)

    def _setup_scroll_area(self):
        """스크롤 영역 설정 메서드"""
        
        scroll_layout = QVBoxLayout()
        self.available_faces_list = AvailableFacesListWidget()
        self.available_faces_list.setFixedWidth(200)
        
        scroll_layout.addWidget(self.available_faces_list)
        
        return scroll_layout

    def _setup_face_registration_layout(self):
        """얼굴 등록 레이아웃 설정 메서드"""
        face_registration_layout = QVBoxLayout()
        
        text_layout = self.setup_text_layout()
        image_layout = self.setup_image_layout()
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_face)
        
        face_registration_layout.addLayout(text_layout)
        face_registration_layout.addLayout(image_layout)
        face_registration_layout.addWidget(add_button)
        
        return face_registration_layout

    def setup_text_layout(self):
        """텍스트 입력 레이아웃 설정 메서드"""
        text_layout = QVBoxLayout()
        
        self.face_name_input = QLineEdit()
        text_layout.addWidget(self.face_name_input)
        
        return text_layout

    def setup_image_layout(self):
        """이미지 업로드 레이아웃 설정 메서드"""
        image_layout = QVBoxLayout()
        
        self.face_image_label = QLabel()
        self.face_image_label.setFixedSize(200, 200)
        self.face_image_label.setAlignment(Qt.AlignCenter)
        
        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)
        
        image_layout.addWidget(self.face_image_label)
        image_layout.addWidget(upload_button)
        
        return image_layout

    def add_face(self):
        """얼굴 추가 메서드"""
        face_name = self.face_name_input.text()
        self.face_setting_processor.add_person_face(face_name)
        
        # 이미 리스트에 있는지 확인
        if self.available_faces_list.findItems(face_name, Qt.MatchExactly):
            print(f"'{face_name}' is already in the list.")
            return

        self.face_setting_processor.add_person_encoding(face_name, self.filepath)
        self.face_setting_processor.save_person_face()
        self.filepath = None
        self.available_faces_list.addItem(face_name)
        self.added_face.emit(face_name)  # 신호 발생
        self.face_name_input.clear()

    def upload_image(self):
        """이미지 업로드 메서드"""
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Upload Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options
        )
        
        if filepath:
            self.filepath = filepath
            pixmap = QPixmap(filepath)
            self.face_image_label.setPixmap(
                pixmap.scaled(self.face_image_label.width(), self.face_image_label.height(), Qt.KeepAspectRatio)
            )
