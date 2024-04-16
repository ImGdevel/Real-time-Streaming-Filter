from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSplitter, QCheckBox
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from utils import Colors
from views.component import AddFaceDialog, FilterListWidget, RegisteredFacesListWidget, AvailableFacesListWidget
from controllers import FilterSettingController, PersonFaceSettingController


class FilterSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_filter = None
        self.selected_filtering_object = [] 
        self.filter_setting_processor = FilterSettingController()
        self.face_setting_processor = PersonFaceSettingController()
        self.face_setting_processor.load_person_faces()
        self.filter_setting_processor.add_filter("MyFilter")

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
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Filter List 라벨
        filter_label = QLabel("Filter List")
        filter_label.setAlignment(Qt.AlignCenter)
        filter_label.setStyleSheet("font-weight: bold;")

        # Filter 목록
        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.onClickItemEvent.connect(self.filter_list_btn_event)  # 새로운 시그널에 연결
        for filter in self.filter_setting_processor.get_filters():
            self.filter_list_widget.add_item(filter.name)

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
        
        # RegisteredFacesListWidget 초기화 및 설정
        self.registered_faces_list_widget = RegisteredFacesListWidget()
        self.registered_faces_list_widget.onClickItemEvent.connect(self.select_registered_face)
        
        # AvailableFacesListWidget 초기화 및 설정
        self.available_faces_list_widget = AvailableFacesListWidget(self.face_setting_processor)
        self.available_faces_list_widget.onClickItemEvent.connect(self.register_face)
        
        face_register_layout.addWidget(self.registered_faces_list_widget)
        face_register_layout.addWidget(self.available_faces_list_widget) 
        
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
        
        self.object_setting_widget = QWidget()
        self.object_setting_widget.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')  # 배경색 설정

        # QVBoxLayout을 self.object_setting_widget 위젯에 설정
        self.object_setting_layout = QVBoxLayout(self.object_setting_widget)
        
        # 토글 버튼(체크박스 스타일) 추가
        self.toggle_button1 = QPushButton("Tobacco")
        self.toggle_button2 = QPushButton("Knife")
        self.toggle_button3 = QPushButton("Bloodshed")
        self.toggle_button4 = QPushButton("Explicit_Content")
        
        # 버튼에 고유한 식별자 부여
        self.toggle_button1.setObjectName("Tobacco")
        self.toggle_button2.setObjectName("Knife")
        self.toggle_button3.setObjectName("Bloodshed")
        self.toggle_button4.setObjectName("Explicit_Content")
        
        # 버튼 클릭 이벤트 연결
        self.toggle_button1.clicked.connect(self.toggle_button_clicked)
        self.toggle_button2.clicked.connect(self.toggle_button_clicked)
        self.toggle_button3.clicked.connect(self.toggle_button_clicked)
        self.toggle_button4.clicked.connect(self.toggle_button_clicked)

        # 현재 선택된 객체 필터링 설정
        self.selected_filtering_object = []

        # 버튼 위젯들을 QVBoxLayout에 추가
        self.object_setting_layout.addWidget(self.toggle_button1)
        self.object_setting_layout.addWidget(self.toggle_button2)
        self.object_setting_layout.addWidget(self.toggle_button3)
        self.object_setting_layout.addWidget(self.toggle_button4)

        object_layout.addWidget(object_label)
        object_layout.addWidget(self.object_setting_widget)
        
        return object_layout

    def toggle_button_clicked(self):
        """토글 버튼(체크박스 스타일) 클릭 이벤트 핸들러"""
        sender_button = self.sender()  # 이벤트를 발생시킨 버튼 가져오기
        button_name = sender_button.objectName()  # 버튼의 고유한 식별자 가져오기

        # 버튼의 스타일 변경
        if button_name in self.selected_filtering_object:
            sender_button.setStyleSheet(f'background-color: {Colors.baseColor00}; color: white;')  # 선택되지 않은 상태의 스타일
            self.selected_filtering_object.remove(button_name)  # 리스트에서 제거
        else:
            sender_button.setStyleSheet(f'background-color: {Colors.baseColor01}; color: white;')  # 선택된 상태의 스타일
            self.selected_filtering_object.append(button_name)  # 리스트에 추가

    
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
        apply_button.clicked.connect(self.apply_filter_settings)
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
        print(item)
        face_name = item
        
        # 중복 체크
        if self.registered_faces_list_widget.findItems(face_name, Qt.MatchExactly):
            print(f"'{face_name}' is already registered.")
            return
        
        # 등록
        self.registered_faces_list_widget.add_item(face_name)

    def select_registered_face(self, item):
        """등록된 얼굴 선택 메서드"""
        pass

    def add_filter(self):
        """Filter 추가 메서드"""
        filter_name = f"Filter {self.filter_list_widget.count() + 1}"
        self.filter_setting_processor.add_filter(filter_name)
        self.filter_list_widget.add_item(filter_name)

    def delete_filter(self):
        """Filter 삭제 메서드"""
        selected_items = self.filter_list_widget.selectedItems()
        for item in selected_items:
            index = self.filter_list_widget.row(item)
            self.filter_list_widget.takeItem(index)

    def filter_list_btn_event(self, text):
        """Filter 버튼 클릭 이벤트 메서드"""
        if text:
            filter_name = text
            self.set_current_filter(filter_name)
            print(f"Button '{filter_name}' clicked.")

    def set_current_filter(self, filter_name):
        """현제 선택된 필터로 창 업데이트"""

        
        self.current_filter = filter_name
        filter_data = self.filter_setting_processor.get_filter(filter_name)

        if filter_data is None:
            # todo : filter가 없는 경우 로직
            pass

        if filter_data:
            print(f"Filter data for '{filter_name}': {filter_data}")
            self.update_registered_faces_list_widget(filter_data.face_filter)
            self.update_object_setting_list(filter_data.object_filter)

        else:
            print(f"Filter '{filter_name}' not found")

        
    def update_registered_faces_list_widget(self, face_filter_data):
        """registered_faces_list_widget 업데이트 메서드"""
        # 기존 항목 삭제
        self.registered_faces_list_widget.clear()
        self.registered_faces_list_widget
        
        # face_filter_data를 QListWidget에 추가
        for face_name in face_filter_data:
            self.registered_faces_list_widget.add_item(face_name)

    def update_object_setting_list(self, filtering_object_datas):
        """_object_setting_list 업데이트 메서드"""
        
        # 기존 버튼들의 스타일만 업데이트
        for i in range(self.object_setting_layout.count()):
            button = self.object_setting_layout.itemAt(i).widget()
            if button.objectName() in filtering_object_datas:
                button.setStyleSheet(f'background-color: {Colors.baseColor01}; color: white;')  # 선택된 상태의 스타일
                button.setChecked(True)  # 버튼을 체크 상태로 설정
            else:
                button.setStyleSheet(f'background-color: {Colors.baseColor02}; color: white;')  # 선택되지 않은 상태의 스타일
                button.setChecked(False)  # 버튼을 체크 해제 상태로 설정

        # selected_filtering_object 업데이트
        self.selected_filtering_object = filtering_object_datas.copy()



    def show_add_face_dialog(self):
        """얼굴 추가 다이얼로그 표시 메서드"""
        dialog = AddFaceDialog(self)
        dialog.added_face.connect(self.update_available_faces)
        dialog.exec_()

    def update_available_faces(self, face_name):
        """available_faces_list_widget 업데이트 메서드"""
        if face_name not in self.available_faces_list_widget.get_items_text():
            self.available_faces_list_widget.add_item(face_name)

    def add_new_face(self):
        """얼굴 추가 메서드"""
        self.show_add_face_dialog()

    def apply_filter_settings(self):
        """세팅된 필터링 정보 저장"""
        # registered_faces_list_widget의 내용 가져오기
        updated_face_filter = self.registered_faces_list_widget.get_items_text()
        updated_filtering_object = self.selected_filtering_object
        # 현재 선택된 필터 정보 업데이트
        self.filter_setting_processor.update_filter(self.current_filter, self.current_filter, True ,updated_face_filter, updated_filtering_object)
        self.face_setting_processor.save_person_face()
        






