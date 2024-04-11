from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QListWidget, QListWidgetItem, QScrollArea
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

        # Filter 목록
        self.filter_list_widget = QListWidget()
        self.filter_list_widget.setStyleSheet(f'background-color: {Colors.baseColor02};')  # 스크롤 뷰 배경색 설정
        self.filter_list_widget.setSpacing(10)  # 아이템 간의 간격 설정

        # 기존 필터 추가
        for filter_name in ["Filter 1", "Filter 2", "Filter 3"]:
            self.add_filter(filter_name)

        # Add Filter, Delete Filter 버튼
        add_button = QPushButton("Add Filter")
        add_button.clicked.connect(self.add_filter)

        delete_button = QPushButton("Delete Filter")
        delete_button.clicked.connect(self.delete_filter)

        left_layout.addWidget(filter_label)
        left_layout.addWidget(self.filter_list_widget)
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

    def add_filter(self, filter_name=None):
        """Filter 추가 메서드"""
        if not filter_name:
            filter_name = f"Filter {self.filter_list_widget.count() + 1}"
        
        button = QPushButton(filter_name)
        button.clicked.connect(self.filter_list_btn_event)
        button.setStyleSheet(f'background-color: {Colors.baseColor01}; color: white;')
        button.setFixedSize(155, 40)  # 버튼 크기 설정
        
        item = QListWidgetItem()
        self.filter_list_widget.addItem(item)
        self.filter_list_widget.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())


    def delete_filter(self):
        """Filter 삭제 메서드"""
        selected_items = self.filter_list_widget.selectedItems()
        for item in selected_items:
            index = self.filter_list_widget.row(item)
            self.filter_list_widget.takeItem(index)

    def filter_list_btn_event(self):
        """Filter 버튼 클릭 이벤트 메서드"""
        button = self.sender()
        if button:
            filter_name = button.text()
            print(f"Button '{filter_name}' clicked.")
