from PySide6.QtWidgets import ( 
    QWidget, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QCheckBox, QLabel, QListWidget, QListWidgetItem, QSplitter, QSlider ,QComboBox, 
    QCheckBox, QLineEdit, QApplication, QMessageBox, QStackedWidget, QSizePolicy, QDialog
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon, QFont
from views.component import (
    PersonFaceDialog, FilterListWidget, RegisteredFacesListWidget, AvailableFacesListWidget, 
    TitleEdit, ShadowWidget, ObjectFilterSettngWidget, MosaicSettingWidget
)
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors, Style


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        
        layout = QVBoxLayout()
        self.label = QLabel("Settings Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


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
        left_layout = self.setup_left_layer()

        # 오른쪽 레이어 - Filter Setting
        self.right_layout = self.setup_right_layer()

        self.empty_layout = QWidget()

        # 전체 레이아웃에 왼쪽과 오른쪽 레이어 추가
        layout.addWidget(left_layout, 1)
        layout.addWidget(self.right_layout, 4)
        layout.addWidget(self.empty_layout, 4)
        self.show_filter_setting_page(False)

        self.setLayout(layout)

    # 왼쪽 레이어
    def setup_left_layer(self):
        """왼쪽 레이어 설정 메서드"""
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        
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

        frame.setLayout(left_layout)

        return frame

    # 오른쪽 레이어
    def setup_right_layer(self):
        """오른쪽 레이어 설정 메서드"""
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        
        right_layout = QVBoxLayout()
        
        # 필터 이름 표시 및 수정
        self.filter_title_label = TitleEdit()
        self.filter_title_label.setMaximumHeight(50)
        self.filter_title_label.onEditEvent.connect(self.update_filter_name)

        # 설정 내용
        content_frame = QFrame()
        content_frame.setLayout(self.setting_page())
        
        #apply_button = QPushButton("적용")
        #apply_button.clicked.connect(self.apply_filter_settings)
        #apply_button.setFixedSize(60, 30)  # 높이 설정
        
        #cancel_button = QPushButton("취소")
        #cancel_button.clicked.connect(self.apply_filter_settings)
        #cancel_button.setFixedSize(60, 30)  # 높이 설정

        # 수평 레이아웃 생성 및 오른쪽 정렬
        #button_layout = QHBoxLayout()
        #button_layout.addStretch(1)
        #button_layout.addWidget(apply_button)
        #button_layout.addWidget(cancel_button)

        # 수평 레이아웃을 오른쪽 레이아웃에 추가
        right_layout.addWidget(self.filter_title_label)
        right_layout.addWidget(content_frame)
        #right_layout.addLayout(button_layout)
        
        right_layout.setStretch(0, 1)  # 상단 버튼 레이아웃 높이 비율
        right_layout.setStretch(1, 3)  # 중단 비디오 옵션 설정 높이 비율
        right_layout.setStretch(2, 4)  # 하단 필터 리스트 높이 비율
        
        frame.setLayout(right_layout)
        return frame
    
    # 세팅 페이지
    def setting_page(self):
        #설정창 들
        face_widget = QWidget()
        face_widget.setStyleSheet(Style.frame_style_none_line)
        face_widget.setLayout(self.setup_face_layout())

        self.object_filter_widget = ObjectFilterSettngWidget()
        self.object_filter_widget.onEventUpdateCheckbox.connect(self.update_object_filter)
        
        mosaic_setting_widget = MosaicSettingWidget()

        # 설정창 스택
        self.settings_content = QStackedWidget(self)
        self.settings_content.addWidget(face_widget)
        self.settings_content.addWidget(self.object_filter_widget)
        self.settings_content.addWidget(mosaic_setting_widget)

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
            self.registered_faces_list_widget.set_filter(self.current_filter)
            self.registered_faces_list_widget.update_list()

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
        
        # 얼굴 등록 박스 설정
        face_register_layout = QHBoxLayout()
        
        # RegisteredFacesListWidget 초기화 및 설정
        registered_faces_list_label = QLabel("필터 등록 인물")
        registered_faces_list_label.setStyleSheet(Style.title_label_middle)
        
        self.registered_faces_list_widget = RegisteredFacesListWidget()
        self.registered_faces_list_widget.set_items_event(self.select_registered_face)
        
        # AvailableFacesListWidget 초기화 및 설정
        available_faces_list_label = QLabel("인물 리스트")
        available_faces_list_label.setStyleSheet(Style.title_label_middle)

        self.available_faces_list_widget = AvailableFacesListWidget()
        self.available_faces_list_widget.set_items_event(self.register_face)
        
        registered_faces_list_layout = QVBoxLayout()
        registered_faces_list_layout.addWidget(registered_faces_list_label)
        registered_faces_list_layout.addWidget(self.registered_faces_list_widget)
        
        available_faces_list_layout = QVBoxLayout()
        available_faces_list_layout.addWidget(available_faces_list_label)
        available_faces_list_layout.addWidget(self.available_faces_list_widget)
        
        face_register_layout.addLayout(registered_faces_list_layout, 2)
        face_register_layout.addLayout(available_faces_list_layout, 1)
        
        face_setting_widget = QWidget()
        face_setting_widget.setLayout(face_register_layout)
        
        face_layout.addWidget(face_label)
        face_layout.addWidget(face_setting_widget)

        # Add 버튼 추가
        add_face_button = QPushButton("등록")
        add_face_button.setFixedSize(60, 30)
        add_face_button.clicked.connect(self.open_person_face_setting_dialog)
        face_layout.addWidget(add_face_button)
        
        self.person_face_setting_window = PersonFaceDialog()
        self.person_face_setting_window.updateEvent.connect(self.update_person_face_setting_dialog_event)
        
        return face_layout

    # 윈도우 디스플레이 설정
    def show_filter_setting_page(self, is_show):
        """윈도우 디스플레이 결정"""
        if is_show:
            self.right_layout.show()
            self.empty_layout.hide()
        else:
            self.right_layout.hide()
            self.empty_layout.show()
            
        # 현재 필터로 창 업데이트
    def set_current_filter(self, filter_name):
        """현제 선택된 필터로 창 업데이트"""
        self.filter_list_widget.update_list()
        filter_data = self.filter_setting_processor.get_filter(filter_name)

        if filter_data:
            print("[Log] : 선택된 필터 > ", filter_data)
            self.filter_list_widget.set_select_item(filter_name)
            self.current_filter = filter_name
            self.filter_title_label.set_title(filter_name)
            #self.filter_title_label.set_show_mode()
            self.current_filter_face_list = filter_data.face_filter
            self.current_filter_object_list = filter_data.object_filter
            self.setup_setting_page(0)
            
            self.show_filter_setting_page(True)
        else:
            print(f"[Log] : Filter '{filter_name}' not found")
            self.show_filter_setting_page(False)


    def register_face(self, person_id):
        """얼굴 등록 메서드"""
        self.registered_faces_list_widget.register_person_faces(person_id)
        self.registered_faces_list_widget.update_list()
   
    
    def select_registered_face(self, item):
        """등록된 얼굴 선택 메서드"""
        
        pass

    # 필터 추가
    def add_filter(self):
        """Filter 추가 메서드"""
        filter_name = self.filter_setting_processor.add_filter()
        self.filter_list_widget.update_list()
        self.set_current_filter(filter_name)

    # 필터 삭제
    def delete_filter(self):
        """Filter 삭제 메서드"""
        self.filter_setting_processor.delete_filter(self.current_filter)
        self.filter_list_widget.update_list()
        self.show_filter_setting_page(False)

    # 인물 등록창 Open
    def open_person_face_setting_dialog(self):
        """얼굴 추가 창을 띄운다."""
        self.person_face_setting_window.show()

    # 얼굴 수정 사항 완료시
    def update_person_face_setting_dialog_event(self):
        """available_faces_list_widget 업데이트 메서드"""
        self.available_faces_list_widget.update_list()
        self.registered_faces_list_widget.update_list()

    # 오브젝트 필터 업데이트
    def update_object_filter(self, list):
        """콜백 오브젝트 리스트 업데이트"""
        self.current_filter_object_list = list

    # 필터 이름 업데이트
    def update_filter_name(self, new_name):
        """필터 이름 변경"""
        if self.current_filter == new_name or new_name == "" or new_name == None:
            #잘못된 입력, 돌아감
            pass
        elif self.filter_setting_processor.get_filter(new_name):
            #필터 이름 중복
            QMessageBox.warning(None, "경고", "이미 존재하는 필터 입니다.", QMessageBox.Ok)
        else:
            #필터 이름 변경
            self.filter_setting_processor.update_filter_name(self.current_filter, new_name)
            self.set_current_filter(new_name)

    # 필터 정보 저장
    def apply_filter_settings(self):
        """세팅된 필터링 정보 저장"""
        # registered_faces_list_widget의 내용 가져오기
        updated_face_filter = self.registered_faces_list_widget.get_items_data()
        updated_filtering_object = self.current_filter_object_list

        # 현재 선택된 필터 정보 업데이트
        self.filter_setting_processor.update_filter(self.current_filter, self.current_filter, True ,updated_face_filter, updated_filtering_object)
        
    # 페이지 리프레쉬
    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        pass
        