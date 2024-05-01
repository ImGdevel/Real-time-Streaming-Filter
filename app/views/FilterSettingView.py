from PySide6.QtWidgets import ( 
    QWidget, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QCheckBox, QLabel, QListWidget, QListWidgetItem, QSplitter, QSlider ,QComboBox, 
    QCheckBox, QLineEdit, QApplication, QMessageBox, QStackedWidget, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont
from views.component import (
    AddFaceDialog, FilterListWidget, RegisteredFacesListWidget, AvailableFacesListWidget, 
    TitleEdit, ShadowWidget, ObjectFilterSettngWidget, MosaicStickerList
)
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors, Style

class FilterSettingView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_setting_processor = FilterSettingController()
        self.face_setting_processor = PersonFaceSettingController()
        self.face_setting_processor.load_person_faces()
        
        self.current_filter = None
        self.current_filter_object_list = [] 
        self.current_filter_face_list = None
        self.current_filter_mosaic_strength = None
        self.current_filter_mosaic_shape = None

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
        self.filter_list_widget.set_items_event(self.set_current_filter)
        
        list_frame_layout.addWidget(list_label)
        list_frame_layout.addWidget(self.filter_list_widget)
        list_frame.setLayout(list_frame_layout)

        filter_list_button_layout = QHBoxLayout()

        # Add Filter, Delete Filter 버튼
        add_button = QPushButton()
        add_button.setIcon(QIcon('./resources/icons/cil-plus.png'))
        add_button.setFixedSize(50,50)
        add_button.setStyleSheet(Style.mini_button_style)
        add_button.clicked.connect(self.add_filter)
        
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('./resources/icons/Orion_bin.png'))
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
        
        # 필터 이름 표시 및 수정
        self.filter_name_widget = TitleEdit()
        self.filter_name_widget.setMaximumHeight(50)
        self.filter_name_widget.onEditEvent.connect(self.update_filter_name)

        # 설정 내용
        content_frame = QFrame()
        content_frame.setLayout(self.setting_page())
        
        apply_button = QPushButton("적용")
        apply_button.clicked.connect(self.apply_filter_settings)
        apply_button.setFixedSize(60, 30)  # 높이 설정
        
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.apply_filter_settings)
        cancel_button.setFixedSize(60, 30)  # 높이 설정

        # 수평 레이아웃 생성 및 오른쪽 정렬
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(apply_button)
        button_layout.addWidget(cancel_button)

        # 수평 레이아웃을 오른쪽 레이아웃에 추가
        right_layout.addWidget(self.filter_name_widget)
        right_layout.addWidget(content_frame)
        right_layout.addLayout(button_layout)
        
        right_layout.setStretch(0, 1)  # 상단 버튼 레이아웃 높이 비율
        right_layout.setStretch(1, 3)  # 중단 비디오 옵션 설정 높이 비율
        right_layout.setStretch(2, 4)  # 하단 필터 리스트 높이 비율
        
        frame.setLayout(right_layout)
        layout.addWidget(frame)
        return layout
    
    # 세팅 페이지
    def setting_page(self):

        #설정창 들
        face_widget = QWidget()
        face_widget.setStyleSheet(Style.frame_style_none_line)
        face_widget.setLayout(self.setup_face_layout())

        self.object_filter_widget = ObjectFilterSettngWidget()
        self.object_filter_widget.onEventUpdateCheckbox.connect(self.update_object_filter)
        
        mos_widget = QWidget()
        mos_widget.setLayout(self.mosaic_setting_layout())

        # 설정창 스택
        self.settings_content = QStackedWidget(self)
        self.settings_content.addWidget(face_widget)
        self.settings_content.addWidget(self.object_filter_widget)
        self.settings_content.addWidget(mos_widget)

        # 설정 목록에 들어갈 버튼 생성
        button1 = QPushButton("필터링 인물 설정")
        button1.setObjectName("setting01")
        button2 = QPushButton("유해매체 필터 설정")
        button2.setObjectName("setting02")
        button3 = QPushButton("모자아크 설정")
        button3.setObjectName("setting03")

        #버튼 연결
        button1.clicked.connect(self.setup_setting_page)
        button2.clicked.connect(self.setup_setting_page)
        button3.clicked.connect(self.setup_setting_page)

        # 버튼을 수직으로 정렬하는 레이아웃 생성
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop)
        vbox.addWidget(button1)
        vbox.addWidget(button2)
        vbox.addWidget(button3)

        # 설정 목록 위젯 생성 및 레이아웃 설정
        settings_list = QWidget()
        settings_list.setStyleSheet(Style.setting_list_button_style)
        settings_list.setMaximumWidth(200)
        settings_list.setLayout(vbox)

        # 메인 윈도우 레이아웃 설정
        layout = QHBoxLayout()
        layout.addWidget(settings_list, 2)
        layout.addWidget(self.settings_content, 5)

        return layout

    def setup_setting_page(self, index):
        button = self.sender()
        buttonName = button.objectName()

        if buttonName == "setting01" or index == 0:
            self.settings_content.setCurrentIndex(0)
            self.update_registered_faces_list_widget(self.current_filter_face_list)

        if buttonName == "setting02" or index == 1:
            self.settings_content.setCurrentIndex(1)
            self.object_filter_widget.setup_object_filter_widget(self.current_filter_object_list)

        if buttonName == "setting03" or index == 2:
            self.settings_content.setCurrentIndex(2)


    # 얼굴 레이어
    def setup_face_layout(self):
        """얼굴 인식 필터 설정 영역 레이아웃 생성"""
        face_layout = QVBoxLayout()
        face_layout.setAlignment(Qt.AlignRight)
        
        face_label = QLabel("필터링 인물 설정")
        face_label.setStyleSheet(Style.title_label)
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
        add_face_button = QPushButton("등록")
        add_face_button.setFixedSize(60, 30)
        add_face_button.clicked.connect(self.show_add_face_dialog)
        face_layout.addWidget(add_face_button)
        
        return face_layout
    
    def mosaic_setting_layout(self):
        """모자이크 설정 레이아웃"""
        layout = QVBoxLayout()

        default_mosaic_layout  = QGridLayout()  # 그리드 레이아웃으로 변경
        default_mosaic_layout.setSpacing(10)  # 위젯 간의 간격을 10으로 설정

        default_mosaic_layout_label = QLabel("기본 모자이크 설정")
        default_mosaic_layout_label.setStyleSheet(Style.title_label)
        default_mosaic_layout.addWidget(default_mosaic_layout_label,0,0)

        # 모자이크 강도 설정 라벨과 슬라이더를 그리드에 추가
        intensity_label = QLabel("모자이크 강도 ")
        intensity_label.setFont(QFont("Arial", 15))  # 폰트 크기 조정
        intensity_slider = QSlider(Qt.Horizontal)  # 수평 슬라이더 생성
        intensity_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # 크기 정책 설정
        intensity_slider.setMaximumWidth(500)  # 최대 너비 설정
        intensity_slider.setMinimumWidth(400)
        default_mosaic_layout .addWidget(intensity_label, 1, 0)  # 라벨을 (0, 0) 위치에 추가
        default_mosaic_layout .addWidget(intensity_slider, 1, 1, alignment=Qt.AlignRight)  # 슬라이더를 (0, 1) 위치에 추가, 우측 정렬 적용

        # 모자이크 모양 설정 라벨과 드롭다운을 그리드에 추가
        shape_label = QLabel("모자이크 모양 ")
        shape_label.setFont(QFont("Arial", 15))  # 폰트 크기 조정
        shape_combobox = QComboBox()
        shape_combobox.setMaximumWidth(300)  # 최대 너비 설정
        shape_combobox.setMinimumWidth(200)
        shape_combobox.addItems(["사각형", "원형"])
        default_mosaic_layout.addWidget(shape_label, 2, 0)  # 라벨을 (1, 0) 위치에 추가
        default_mosaic_layout.addWidget(shape_combobox, 2, 1,  alignment=Qt.AlignRight)  # 드롭다운을 (1, 1) 위치에 추가
        
        default_mosaic_layout.setColumnStretch(0, 1)  # 첫 번째 열의 너비를 1배로 설정
        default_mosaic_layout.setColumnStretch(1, 4)  # 첫 번째 열의 너비를 4배로 설정

        default_mosaic_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

    
        layout.addLayout(default_mosaic_layout)

        return layout

    # 윈도우 디스플레이 설정
    def show_filter_setting_window(self, is_show):
        """윈도우 디스플레이 결정"""
        if is_show:
            self.right_widget.show()
            self.empty_widget.hide()
        else:
            self.right_widget.hide()
            self.empty_widget.show()


    def register_face(self, person_name):
        """얼굴 등록 메서드"""
        if self.registered_faces_list_widget.is_in_item(person_name): #중복 체크
            print(f"'{person_name}' is already registered.")
            return
        
        self.registered_faces_list_widget.add_item(person_name) # 등록
   
    
    def select_registered_face(self, item):
        """등록된 얼굴 선택 메서드"""
        pass

    # 필터 추가
    def add_filter(self):
        """Filter 추가 메서드"""
        # filter_name = "New Filter"
        # for i in range(1, self.filter_list_widget.count() + 2):
        #     filter_name = f"New Filter {i}"
        #     if not self.filter_setting_processor.get_filter(filter_name):
        #         break
        filter_name = self.filter_setting_processor.add_filter()
        print(" add filter : "+filter_name)
        self.filter_list_widget.add_item(filter_name)
        self.set_current_filter(filter_name)

    # 필터 삭제
    def delete_filter(self):
        """Filter 삭제 메서드"""
        self.filter_setting_processor.delete_filter(self.current_filter)
        self.filter_list_widget.delete_item(self.current_filter)
        self.set_current_filter(self.filter_list_widget.get_current_item_text())

    # 현재 필터로 창 업데이트
    def set_current_filter(self, filter_name):
        """현제 선택된 필터로 창 업데이트"""
        filter_data = self.filter_setting_processor.get_filter(filter_name)

        if filter_data:
            print("[Log] : 선택된 필터 > ", filter_data)
            self.current_filter = filter_name
            self.filter_name_widget.set_title(filter_name)
            self.current_filter_face_list = filter_data.face_filter
            self.current_filter_object_list = filter_data.object_filter
            self.setup_setting_page(0)

            self.show_filter_setting_window(True)
        else:
            print(f"[Log] : Filter '{filter_name}' not found")
            self.show_filter_setting_window(False)
            
    # 
    def update_registered_faces_list_widget(self, face_filter_data):
        """registered_faces_list_widget 업데이트 메서드"""
        # 기존 항목 삭제
        self.registered_faces_list_widget.clear()
        # face_filter_data를 QListWidget에 추가
        for face_name in face_filter_data:
            self.registered_faces_list_widget.add_item(face_name)

    # 인물 등록창 Open
    def show_add_face_dialog(self):
        """얼굴 추가 다이얼로그 표시 메서드"""
        dialog = AddFaceDialog(self)
        dialog.updateEvent.connect(self.update_available_faces)
        dialog.exec_()

    # 오브젝트 필터 업데이트
    def update_object_filter(self, list):
        """콜백 오브젝트 리스트 업데이트"""
        self.current_filter_object_list = list

    # 
    def update_available_faces(self):
        """available_faces_list_widget 업데이트 메서드"""
        self.available_faces_list_widget.update_list()

    # 필터 이름 업데이트
    def update_filter_name(self, text):
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

    # 필터 정보 저장
    def apply_filter_settings(self):
        """세팅된 필터링 정보 저장"""
        # registered_faces_list_widget의 내용 가져오기
        updated_face_filter = self.registered_faces_list_widget.get_items_text()
        updated_filtering_object = self.current_filter_object_list

        # 현재 선택된 필터 정보 업데이트
        self.filter_setting_processor.update_filter(self.current_filter, self.current_filter, True ,updated_face_filter, updated_filtering_object)
        
    # 페이지 리프레쉬
    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        pass
        