from utils import Colors, Style
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSplitter, QCheckBox, QLineEdit, QApplication, QMessageBox
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from views.component import AddFaceDialog, FilterListWidget, RegisteredFacesListWidget, AvailableFacesListWidget, TitleEdit, ShadowWidget
from controllers import FilterSettingController, PersonFaceSettingController

class FilterSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_setting_processor = FilterSettingController()
        self.face_setting_processor = PersonFaceSettingController()
        self.face_setting_processor.load_person_faces()
        
        self.current_filter = None
        self.selected_filtering_object = [] 

        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        layout = QHBoxLayout()

        # 왼쪽 레이어 - Filter List
        self.left_layout = self.setup_left_layer()
        self.left_widget = ShadowWidget()
        self.left_widget.setLayout(self.left_layout)

        # 오른쪽 레이어 - Filter Setting
        self.right_layout = self.setup_right_layer()
        self.right_widget = ShadowWidget()
        self.right_widget.setStyleSheet(Style.frame_style)
        self.right_widget.setLayout(self.right_layout)

        self.empty_widget = QFrame()

        # 전체 레이아웃에 왼쪽과 오른쪽 레이어 추가
        layout.addWidget(self.left_widget, 1) 
        layout.addWidget(self.right_widget, 4)  
        layout.addWidget(self.empty_widget, 4)  
        self.show_filter_setting_window(False)

        self.setLayout(layout)

    # 왼쪽 레이어
    def setup_left_layer(self):
        """왼쪽 레이어 설정 메서드"""
        left_layout = QVBoxLayout()
        
        # Filter 목록
        list_frame = QWidget()
        list_frame.setStyleSheet(Style.list_frame_style)
        list_frame_layout = QVBoxLayout()
        
        list_label = QLabel("필터 목록")
        list_label.setStyleSheet(Style.list_frame_label)
        
        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.set_items_event(self.filter_list_btn_event)
        
        list_frame_layout.addWidget(list_label)
        list_frame_layout.addWidget(self.filter_list_widget)
        list_frame.setLayout(list_frame_layout)

        filter_list_button_layout = QHBoxLayout()

        # Add Filter, Delete Filter 버튼
        add_button = QPushButton("Add Filter")
        add_button.setFixedSize(50,50)
        add_button.setStyleSheet(Style.mini_button_style)
        add_button.clicked.connect(self.add_filter)
        
        delete_button = QPushButton("Delete Filter")
        delete_button.setIcon(QIcon('./resources/icons/cil-media-play.png'))
        delete_button.setFixedSize(50,50)
        delete_button.setStyleSheet(Style.mini_button_style)
        delete_button.clicked.connect(self.delete_filter)

        filter_list_button_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        filter_list_button_layout.addWidget(add_button)
        filter_list_button_layout.addSpacing(10)  # 버튼 사이 간격
        filter_list_button_layout.addWidget(delete_button)

        left_layout.addWidget(list_frame)
        left_layout.addLayout(filter_list_button_layout)

        return left_layout

    # 오른쪽 레이어
    def setup_right_layer(self):
        """오른쪽 레이어 설정 메서드"""
        
        layout = QVBoxLayout()
        frame = QFrame()
        right_layout = QVBoxLayout()

        # QSplitter 생성
        splitter = QSplitter(Qt.Vertical)

        # 필터 이름 표시 및 수정
        self.filter_name_widget = TitleEdit()
        self.filter_name_widget.setMaximumHeight(50)
        self.filter_name_widget.onEditEvent.connect(self.change_filter_name)

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
        apply_button.clicked.connect(self.apply_filter_settings)
        apply_button.setFixedSize(60, 30)  # 높이 설정

        # 수평 레이아웃 생성 및 오른쪽 정렬
        apply_layout = QHBoxLayout()
        apply_layout.addStretch(1)
        apply_layout.addWidget(apply_button)

        # 수평 레이아웃을 오른쪽 레이아웃에 추가
        right_layout.addWidget(self.filter_name_widget)
        right_layout.addWidget(splitter)
        right_layout.addLayout(apply_layout)
        
        right_layout.setStretch(0, 1)  # 상단 버튼 레이아웃 높이 비율
        right_layout.setStretch(1, 3)  # 중단 비디오 옵션 설정 높이 비율
        right_layout.setStretch(2, 4)  # 하단 필터 리스트 높이 비율
        
        frame.setLayout(right_layout)
        layout.addWidget(frame)
        return layout


    # 얼굴 레이어
    def setup_face_layout(self):
        """얼굴 인식 필터 설정 영역 레이아웃 생성"""
        face_layout = QVBoxLayout()
        
        face_label = QLabel("Face Filtering")
        face_label.setFixedHeight(30)  # 높이 설정
        
        # 얼굴 등록 박스 설정
        face_register_layout = QHBoxLayout()
        
        # RegisteredFacesListWidget 초기화 및 설정
        self.registered_faces_list_widget = RegisteredFacesListWidget()
        self.registered_faces_list_widget.set_items_event(self.select_registered_face)
        
        # AvailableFacesListWidget 초기화 및 설정
        self.available_faces_list_widget = AvailableFacesListWidget()
        self.available_faces_list_widget.set_items_event(self.register_face)
        
        face_register_layout.addWidget(self.registered_faces_list_widget)
        face_register_layout.addWidget(self.available_faces_list_widget) 
        
        face_setting_widget = QWidget()
        face_setting_widget.setLayout(face_register_layout)
        
        face_layout.addWidget(face_label)
        face_layout.addWidget(face_setting_widget)

        # Add 버튼 추가
        add_face_button = QPushButton("Add")
        add_face_button.setFixedSize(60, 30)
        add_face_button.clicked.connect(self.show_add_face_dialog)
        face_layout.addWidget(add_face_button)
        
        return face_layout

    # 오브젝트 레이어
    def setup_object_layout(self):
        """객체 필터링 설정 영역 레이아웃 생성"""
        object_layout = QVBoxLayout()
        
        object_label = QLabel("Object Filtering")
        object_label.setStyleSheet("font-weight: bold;")
        object_label.setFixedHeight(30)  # 높이 설정
        
        self.object_setting_widget = QWidget()

        # QVBoxLayout을 self.object_setting_widget 위젯에 설정
        self.object_setting_layout = QVBoxLayout(self.object_setting_widget)
        
        # 토글 버튼(체크박스 스타일) 추가
        self.toggle_button1 = QPushButton("담배")
        self.toggle_button1.userData = "smoke"
        self.toggle_button2 = QPushButton("칼")
        self.toggle_button2.userData = "2"
        self.toggle_button3 = QPushButton("?")
        self.toggle_button3.userData = "3"
        self.toggle_button4 = QPushButton("선정성 컨텐츠")
        self.toggle_button4.userData = "4"
        
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
    

    def show_filter_setting_window(self, is_show):
        """윈도우 디스플레이 결정"""
        if is_show:
            self.right_widget.show()
            self.empty_widget.hide()
        else:
            self.right_widget.hide()
            self.empty_widget.show()


    def toggle_button_clicked(self):
        """토글 버튼(체크박스 스타일) 클릭 이벤트 핸들러"""
        sender_button = self.sender()  # 이벤트를 발생시킨 버튼 가져오기
        button_name = sender_button.userData  # 버튼의 고유한 식별자 가져오기

        # 버튼의 스타일 변경
        if button_name in self.selected_filtering_object:
            self.selected_filtering_object.remove(button_name)  # 리스트에서 제거
        else:
            self.selected_filtering_object.append(button_name)  # 리스트에 추가
    

    def register_face(self, person_name):
        """얼굴 등록 메서드"""
        if self.registered_faces_list_widget.is_in_item(person_name): #중복 체크
            print(f"'{person_name}' is already registered.")
            return
        self.registered_faces_list_widget.add_item(person_name) # 등록
    

    def select_registered_face(self, item):
        """등록된 얼굴 선택 메서드"""
        pass

    def add_filter(self):
        """Filter 추가 메서드"""
        filter_name = "New Filter"
        for i in range(1, self.filter_list_widget.count() + 2):
            filter_name = f"New Filter {i}"
            if not self.filter_setting_processor.get_filter(filter_name):
                break
        print(filter_name)
        self.filter_setting_processor.add_filter(filter_name)
        self.filter_list_widget.add_item(filter_name)
        self.set_current_filter(filter_name)


    def delete_filter(self):
        """Filter 삭제 메서드"""
        self.filter_setting_processor.delete_filter(self.current_filter)
        self.filter_list_widget.delete_item(self.current_filter)
        print(self.filter_list_widget.get_current_item_text())
        self.set_current_filter(self.filter_list_widget.get_current_item_text())


    def filter_list_btn_event(self, filter_name):
        """Filter 버튼 클릭 이벤트 메서드"""
        if filter_name:
            self.set_current_filter(filter_name)


    def set_current_filter(self, filter_name):
        """현제 선택된 필터로 창 업데이트"""
        self.current_filter = filter_name
        filter_data = self.filter_setting_processor.get_filter(filter_name)
        print("[Log] : 선택된 필터 > ", filter_data)
        if filter_data:
            self.filter_list_widget.update_filter_list()
            self.update_registered_faces_list_widget(filter_data.face_filter)
            self.update_object_setting_list(filter_data.object_filter)
            self.filter_name_widget.set_title(filter_name)      
            self.show_filter_setting_window(True)
        else:
            print(f"Filter '{filter_name}' not found")
            self.show_filter_setting_window(False)
    
    
    def update_registered_faces_list_widget(self, face_filter_data):
        """registered_faces_list_widget 업데이트 메서드"""
        # 기존 항목 삭제
        self.registered_faces_list_widget.clear()
        # face_filter_data를 QListWidget에 추가
        for face_name in face_filter_data:
            self.registered_faces_list_widget.add_item(face_name)


    def update_object_setting_list(self, filtering_object_datas):
        """_object_setting_list 업데이트 메서드"""
        
        # 기존 버튼들의 스타일만 업데이트
        for i in range(self.object_setting_layout.count()):
            button = self.object_setting_layout.itemAt(i).widget()
            if button.objectName() in filtering_object_datas:
                button.setChecked(True)  # 버튼을 체크 상태로 설정
            else:
                button.setChecked(False)  # 버튼을 체크 해제 상태로 설정

        # selected_filtering_object 업데이트
        self.selected_filtering_object = filtering_object_datas.copy()


    def show_add_face_dialog(self):
        """얼굴 추가 다이얼로그 표시 메서드"""
        dialog = AddFaceDialog(self)
        dialog.added_face.connect(self.update_available_faces)
        dialog.exec_()


    def update_available_faces(self):
        """available_faces_list_widget 업데이트 메서드"""
        self.available_faces_list_widget.update_list()


    def change_filter_name(self, text):
        """필터 이름 변경"""
        if self.current_filter == text or text == "" or text == None:
            #잘못된 입력, 돌아감
            pass
        elif self.filter_setting_processor.get_filter(text):
            #필터 이름 중복
            QMessageBox.warning(None, "경고", "이미 존재하는 필터 입니다.", QMessageBox.Ok)
        else:
            #필터 이름 변경
            filter = self.filter_setting_processor.get_filter(self.current_filter)
            self.filter_setting_processor.update_filter(self.current_filter, text, True ,filter.face_filter, filter.object_filter)
            self.set_current_filter(text)


    def apply_filter_settings(self):
        """세팅된 필터링 정보 저장"""
        # registered_faces_list_widget의 내용 가져오기
        updated_face_filter = self.registered_faces_list_widget.get_items_text()
        updated_filtering_object = self.selected_filtering_object
        # 현재 선택된 필터 정보 업데이트
        self.filter_setting_processor.update_filter(self.current_filter, self.current_filter, True ,updated_face_filter, updated_filtering_object)
        
        
    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_filter_list()
        pass
        