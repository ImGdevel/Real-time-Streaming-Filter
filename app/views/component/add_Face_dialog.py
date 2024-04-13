from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap


class AddFaceDialog(QDialog):
    added_face = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Face")
        self.setFixedSize(600, 400)

        main_layout = QHBoxLayout()

        # Scroll Area with Filter List
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        self.available_faces_list = QListWidget()
        self.available_faces_list.addItems(["People 1", "People 2", "사람 3"])  # 임시 데이터
        scroll_layout.addWidget(self.available_faces_list)

        scroll_area.setWidget(scroll_content)
        
        
        # Face Registration Layout
        face_registration_layout = QVBoxLayout()
        
        # Text Area and Add Button
        text_layout = QVBoxLayout()
        
        self.face_name_input = QLineEdit()
        text_layout.addWidget(self.face_name_input)
        face_registration_layout.addLayout(text_layout)

        # Image Area
        image_layout = QVBoxLayout()
        
        self.face_image_label = QLabel()
        self.face_image_label.setFixedSize(200, 200)
        self.face_image_label.setAlignment(Qt.AlignCenter)
        
        upload_button = QPushButton("Upload Image")
        upload_button.clicked.connect(self.upload_image)
        image_layout.addWidget(self.face_image_label)
        image_layout.addWidget(upload_button)
        
        face_registration_layout.addLayout(image_layout)
        
        add_button = QPushButton("Add")
        add_button.clicked.connect(self.add_face)
        face_registration_layout.addWidget(add_button)
    
        

        # Combine Layouts
        main_layout.addWidget(scroll_area)
        main_layout.addLayout(face_registration_layout)
        
        
        self.setLayout(main_layout)

    def add_face(self):
        """얼굴 추가 메서드"""
        face_name = self.face_name_input.text()

        # 중복 체크
        if self.available_faces_list.findItems(face_name, Qt.MatchExactly):
            print(f"'{face_name}' is already in the list.")
            return

        # 추가
        self.available_faces_list.addItem(face_name)
        self.added_face.emit(face_name)
        self.face_name_input.clear()

    def upload_image(self):
        """사진 업로드 메서드"""
        options = QFileDialog.Options()
        filepath, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Images (*.png *.jpg *.jpeg);;All Files (*)", options=options)
        
        if filepath:
            pixmap = QPixmap(filepath)
            self.face_image_label.setPixmap(pixmap.scaled(self.face_image_label.width(), self.face_image_label.height(), Qt.KeepAspectRatio))
