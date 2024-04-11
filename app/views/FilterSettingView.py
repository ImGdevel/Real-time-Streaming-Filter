from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QComboBox, QScrollArea, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from utils import Colors

class FilterSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        self.layout = QHBoxLayout()

        # 왼쪽 레이어 - Filter List
        self.left_layout = self.setup_left_layer()
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)
        self.left_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 왼쪽 레이어 배경색 설정

        # 오른쪽 레이어 - Filter Setting
        self.right_layout = self.setup_right_layer()
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 오른쪽 레이어 배경색 설정

        # 전체 레이아웃에 왼쪽과 오른쪽 레이어 추가
        self.layout.addWidget(self.left_widget, 1)  # 왼쪽 레이어 크기를 1로 설정
        self.layout.addWidget(self.right_widget, 4)  # 오른쪽 레이어 크기를 4로 설정

        self.setLayout(self.layout)

    def setup_left_layer(self):
        """왼쪽 레이어 설정 메서드"""
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)  # 여백 설정

        # Filter List 라벨
        filter_label = QLabel("Filter List")
        filter_label.setAlignment(Qt.AlignCenter)
        filter_label.setStyleSheet("font-weight: bold;")

        # Filter 목록 스크롤 뷰
        self.filter_list_widget = QListWidget()
        self.filter_list_widget.setStyleSheet(f"background-color: {Colors.baseColor02};")  # 스크롤 뷰 배경색 설정
        self.filter_list_widget.addItems(["Filter 1", "Filter 2", "Filter 3"])  # 임시 필터 목록
        
        # Add Filter 버튼
        add_button = QPushButton("Add Filter")
        add_button.clicked.connect(self.add_filter)

        # Delete Filter 버튼
        delete_button = QPushButton("Delete Filter")
        delete_button.clicked.connect(self.delete_filter)

        left_layout.addWidget(filter_label)
        
        # 스크롤 뷰에 필터 목록 추가
        filter_scroll = QScrollArea()
        filter_scroll.setWidget(self.filter_list_widget)
        filter_scroll.setWidgetResizable(True)
        left_layout.addWidget(filter_scroll)

        left_layout.addWidget(add_button)
        left_layout.addWidget(delete_button)

        return left_layout

    def setup_right_layer(self):
        """오른쪽 레이어 설정 메서드"""
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)  # 여백 설정

        # 얼굴 인식 필터 설정
        face_label = QLabel("Face Filtering")
        face_label.setStyleSheet("font-weight: bold;")

        # 얼굴 인식 필터 설정 공간 (임시로 QLabel로 표시)
        face_setting_label = QLabel("Face Filter Setting Area")

        # 객체 필터링 설정
        object_label = QLabel("Object Filtering")
        object_label.setStyleSheet("font-weight: bold;")

        # 객체 필터링 설정 공간 (임시로 QLabel로 표시)
        object_setting_label = QLabel("Object Filter Setting Area")

        right_layout.addWidget(face_label)
        right_layout.addWidget(face_setting_label)
        right_layout.addWidget(object_label)
        right_layout.addWidget(object_setting_label)

        return right_layout

    def add_filter(self):
        """Filter 추가 메서드"""
        new_filter = f"Filter {self.filter_list_widget.count() + 1}"
        item = QListWidgetItem(new_filter)
        self.filter_list_widget.addItem(item)

    def delete_filter(self):
        """Filter 삭제 메서드"""
        selected_items = self.filter_list_widget.selectedItems()
        for item in selected_items:
            self.filter_list_widget.takeItem(self.filter_list_widget.row(item))

    def change_filter_setting(self, index):
        """Filter 설정 변경 메서드"""
        # Filter 선택에 따른 설정 변경 로직 추가
        pass

    def apply_filter_setting(self):
        """Filter 설정 적용 메서드"""
        # Filter 설정 적용 로직 추가
        pass
