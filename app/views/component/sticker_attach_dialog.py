from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon, QImage
from models.replace_manager import ReplaceManager
from utils import Style
import cv2
import np

class RegisteredFaceViewDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(Style.frame_style)
        self.replace_manager = ReplaceManager()
        self._initUI()

    def _initUI(self):
        self.setWindowTitle("Registered Face View")
        self.setFixedSize(320, 400)

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        register_button = QPushButton()
        register_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        register_button.setIcon(QIcon('./resources/icons/cil-folder-open'))
        register_button.setFixedSize(40, 40)
        register_button.clicked.connect(self.register_image)
        main_layout.addWidget(register_button)

        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 300)
        self.image_label.setStyleSheet("border: 2px solid #808080")
        main_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        save_button = QPushButton("등록")
        save_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        save_button.clicked.connect(self.save)
        button_layout.addWidget(save_button)

        cancel_button = QPushButton("취소")
        cancel_button.setStyleSheet("border: 2px solid #808080; padding: 5px")
        cancel_button.clicked.connect(self.cancel)
        button_layout.addWidget(cancel_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def set_sticker_dialog(self, id=None):
        """이미 등록된 스티커가 있다면 불러오기"""
        if id is not None:
            img = self.replace_manager.load_img_to_id(id)
            print(img)
            if img is not None:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                qimg = QImage(img_rgb.data, img_rgb.shape[1], img_rgb.shape[0], img_rgb.strides[0], QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(qimg)
                self.image_label.setPixmap(pixmap)
                self.image_label.setScaledContents(True)

    def register_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Image Files (*.png *.jpeg)", options=options
        )

        if file_path:
            self.image_path = file_path
            self.load_image(file_path)

    def load_image(self, file_path):
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    def save(self):
        if hasattr(self, 'image_path'):
            print("스티커 등록")
            self.replace_manager.register_img_path(self.image_path)
        self.close()

    def cancel(self):
        self.close()


    def drag_enter_event(self, event):
        """드래그 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drag_move_event(self, event):
        """드래그 이동 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """드롭 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            
            image_files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.add_face_process(image_files)
        else:
            event.ignore()

