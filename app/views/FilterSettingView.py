from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSplitter
from PyQt5.QtCore import Qt, QTimer
from utils import Colors
from views.component import AddFaceDialog

class FilterSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.current_filter = None

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

    def setup_face_layout(self):
        """얼굴 인식 필터 설정 영역 레이아웃 생성"""
        face_layout = QVBoxLayout()
        
        face_label = QLabel("Face Filtering")
        face_label.setStyleSheet("font-weight: bold;")
        face_label.setFixedHeight(30)  # 높이 설정
        
        # 얼굴 등록 박스 설정
        face_register_layout = QHBoxLayout()
        
        # 등록되지 않은 얼굴 목록
        self.available_faces_list = QListWidget()
        self.available_faces_list.addItems(["Face 1", "Face 2", "Face 3"])  # 임시 데이터
        self.available_faces_list.itemClicked.connect(self.register_face)
        
        # 등록된 얼굴 목록
        self.registered_faces_list = QListWidget()
        self.registered_faces_list.itemClicked.connect(self.select_registered_face)
        
        face_register_layout.addWidget(self.registered_faces_list)  # 등록된 얼굴 목록을 먼저 추가
        face_register_layout.addWidget(self.available_faces_list)  # 등록되지 않은 얼굴 목록을 그 다음에 추가
        
        face_setting_widget = QWidget()
        face_setting_widget.setLayout(face_register_layout)
        face_setting_widget.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')  # 배경색 설정
        
        face_layout.addWidget(face_label)
        face_layout.addWidget(face_setting_widget)

        # Add 버튼 추가
        add_face_button = QPushButton("Add")
        add_face_button.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')
        add_face_button.setFixedSize(60, 30)
        add_face_button.clicked.connect(self.show_add_face_dialog)
        face_layout.addWidget(add_face_button)
        
        return face_layout


    def setup_object_layout(self):
        """객체 필터링 설정 영역 레이아웃 생성"""
        object_layout = QVBoxLayout()
        
        object_label = QLabel("Object Filtering")
        object_label.setStyleSheet("font-weight: bold;")
        object_label.setFixedHeight(30)  # 높이 설정
        
        object_setting_widget = QWidget()
        object_setting_widget.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')  # 배경색 설정
        
        object_layout.addWidget(object_label)
        object_layout.addWidget(object_setting_widget)
        
        return object_layout

    def setup_right_layer(self):
        """오른쪽 레이어 설정 메서드"""
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(10, 10, 10, 10)  # 여백 설정

        # QSplitter 생성
        splitter = QSplitter(Qt.Vertical)

        # 얼굴 인식 필터 설정 영역
        face_widget = QWidget()
        face_widget.setLayout(self.setup_face_layout())
        
        # 객체 필터링 설정 영역
        object_widget = QWidget()
        object_widget.setLayout(self.setup_object_layout())
        
        # QSplitter에 위젯 추가
        splitter.addWidget(face_widget)
        splitter.addWidget(object_widget)

        # todo: 하단 오른 쪽 끝에 적용 버튼 추가
        apply_button = QPushButton("적용")
        apply_button.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')  # 배경색 설정
        apply_button.setFixedSize(60, 30)  # 높이 설정

        # 수평 레이아웃 생성 및 오른쪽 정렬
        apply_layout = QHBoxLayout()
        apply_layout.addStretch(1)
        apply_layout.addWidget(apply_button)

        # 수평 레이아웃을 오른쪽 레이아웃에 추가
        right_layout.addWidget(splitter)
        right_layout.addLayout(apply_layout)

        # splitter.setSizes를 이 위치로 이동
        def set_splitter_sizes():
            splitter.setSizes([int(self.width() * 5 / 9), int(self.width() * 4 / 9)])
        
        # widget이 나타난 후에 호출되도록 QTimer를 사용
        QTimer.singleShot(0, set_splitter_sizes)
        
        return right_layout

    def register_face(self, item):
        """얼굴 등록 메서드"""
        face_name = item.text()
        
        # 중복 체크
        if self.registered_faces_list.findItems(face_name, Qt.MatchExactly):
            print(f"'{face_name}' is already registered.")
            return
        
        # 등록
        self.registered_faces_list.addItem(face_name)

    def select_registered_face(self, item):
        """등록된 얼굴 선택 메서드"""
        pass

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
            
    def show_add_face_dialog(self):
        """얼굴 추가 다이얼로그 표시 메서드"""
        dialog = AddFaceDialog(self)
        dialog.added_face.connect(self.update_available_faces)
        dialog.exec_()

    def update_available_faces(self, face_name):
        """available_faces_list 업데이트 메서드"""
        if face_name not in [self.available_faces_list.item(i).text() for i in range(self.available_faces_list.count())]:
            self.available_faces_list.addItem(face_name)

    def add_new_face(self):
        """얼굴 추가 메서드"""
        self.show_add_face_dialog()
