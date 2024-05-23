from PySide6.QtWidgets import ( 
    QWidget, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout, QGridLayout, 
    QPushButton, QCheckBox, QLabel, QListWidget, QListWidgetItem, QSplitter, QSlider ,QComboBox, QButtonGroup,
    QCheckBox, QLineEdit, QApplication, QMessageBox, QStackedWidget, QSizePolicy, QDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QIcon, QFont, QValidator
from views.component import (
    PersonFaceDialog, FilterListWidget, RegisteredFacesListWidget, AvailableFacesListWidget, 
    TitleEdit, ObjectFilterSettngWidget, BlurSettingWidget, ContentLabeling
    , DetectSettingWidget
)
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors, Style, Icons


class FilterSettingView(QWidget):
    webcam_on = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)

        self.filter_setting_processor = FilterSettingController()
        self.face_setting_processor = PersonFaceSettingController()
        self.face_setting_processor.load_person_faces()
        
        self.current_filter = None

        self.initUI()

    def initUI(self):
        # 전체 레이아웃 설정
        layout = QHBoxLayout()

        # 왼쪽 레이어 - Filter List
        left_layout = self.setup_left_layer()
        
        # 오른쪽 레이어 - Filter Setting
        empty_layout = QWidget()
        right_layout = self.setup_right_layer()
        
        self.stacked_layout = QStackedWidget()
        self.stacked_layout.addWidget(right_layout)
        self.stacked_layout.addWidget(empty_layout)

        # 전체 레이아웃에 왼쪽과 오른쪽 레이어 추가
        layout.addWidget(left_layout, 1)
        layout.addWidget(self.stacked_layout, 4)
        self.show_filter_setting_page(False)

        self.setLayout(layout)

    # 왼쪽 레이어
    def setup_left_layer(self):
        """왼쪽 레이어 설정 메서드"""
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        frame.setMinimumWidth(200)
        
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
        add_button.setToolTip('새 필터')
        add_button.setIcon(QIcon(Icons.plus))
        add_button.setFixedSize(50,50)
        add_button.setStyleSheet(Style.mini_button_style)
        add_button.clicked.connect(self.add_filter)
        
        delete_button = QPushButton()
        delete_button.setToolTip('필터 삭제')
        delete_button.setIcon(QIcon(Icons.dust_bin))
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
        content_frame = QWidget()
        content_frame.setLayout(self.setting_page())

        # 수평 레이아웃을 오른쪽 레이아웃에 추가
        right_layout.addWidget(self.filter_title_label)
        right_layout.addWidget(content_frame)
        
        right_layout.setStretch(0, 1)  # 상단 버튼 레이아웃 높이 비율
        right_layout.setStretch(1, 3)  # 중단 비디오 옵션 설정 높이 비율
        right_layout.setStretch(2, 4)  # 하단 필터 리스트 높이 비율
        
        frame.setLayout(right_layout)
        return frame
    
    # 세팅 페이지
    def setting_page(self):
        #설정창 들
        face_widget = self.setup_face_layout()

        self.object_filter_widget = ObjectFilterSettngWidget()
        
        self.mosaic_setting_widget = BlurSettingWidget()
        
        self.detect_setting_widget = DetectSettingWidget()
        
        content01 =  ContentLabeling()
        content01.setLabel("필터링 인물 설정")
        content01.setContent(face_widget)
        
        content02 =  ContentLabeling()
        content02.setLabel("유해 매체 필터링 설정")
        content02.setContent(self.object_filter_widget)
        
        content03 =  ContentLabeling()
        content03.setLabel("모자이크 블러 설정")
        content03.setContent(self.mosaic_setting_widget)
        
        content04 =  ContentLabeling()
        content04.setLabel("감지 정확도 설정")
        content04.setContent(self.detect_setting_widget)


        # 설정창 스택
        self.settings_content = QStackedWidget(self)
        self.settings_content.addWidget(content01)
        self.settings_content.addWidget(content02)
        self.settings_content.addWidget(content03)
        self.settings_content.addWidget(content04)
    
        # 설정 목록에 들어갈 버튼 생성
        self.button1 = QPushButton("필터링 인물")
        self.button1.setObjectName("setting01")
        self.button1.setMinimumHeight(45)
        self.button1.setCheckable(True)
        self.button2 = QPushButton("유해 매체 필터링")
        self.button2.setObjectName("setting02")
        self.button2.setMinimumHeight(45)
        self.button2.setCheckable(True)
        self.button3 = QPushButton("모자아크 블러")
        self.button3.setObjectName("setting03")
        self.button3.setMinimumHeight(45)
        self.button3.setCheckable(True)
        self.button4 = QPushButton("감지 정확도")
        self.button4.setObjectName("setting03")
        self.button4.setMinimumHeight(45)
        self.button4.setCheckable(True)

        #버튼 연결
        self.button1.clicked.connect(lambda: self.setup_setting_page(0))
        self.button2.clicked.connect(lambda: self.setup_setting_page(1))
        self.button3.clicked.connect(lambda: self.setup_setting_page(2))
        self.button4.clicked.connect(lambda: self.setup_setting_page(3))
        
        button_group = QButtonGroup()
        button_group.setExclusive(False)
        button_group.addButton(self.button1)
        button_group.addButton(self.button2)
        button_group.addButton(self.button3)
        button_group.addButton(self.button4)
        
        # 버튼을 수직으로 정렬하는 레이아웃 생성
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0,2,0,0)
        vbox.setAlignment(Qt.AlignTop)
        vbox.addWidget(self.button1)
        vbox.addWidget(self.button2)
        vbox.addWidget(self.button3)
        vbox.addWidget(self.button4)

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
            
        if index == 0:
            self.settings_content.setCurrentIndex(0)
            self.registered_faces_list_widget.set_filter(self.current_filter)
            self.registered_faces_list_widget.update_list()
            self.button1.setChecked(True)
            self.button2.setChecked(False)
            self.button3.setChecked(False)
            self.button4.setChecked(False)
        
        elif index == 1:
            self.settings_content.setCurrentIndex(1)
            self.object_filter_widget.setup_object_filter_widget(self.current_filter)
            self.button2.setChecked(True)
            self.button1.setChecked(False)
            self.button3.setChecked(False)
            self.button4.setChecked(False)

        elif index == 2:
            self.settings_content.setCurrentIndex(2)
            self.mosaic_setting_widget.setup_mosaic_setting(self.current_filter)
            self.button3.setChecked(True)
            self.button2.setChecked(False)
            self.button1.setChecked(False)
            self.button4.setChecked(False)
            
        elif index == 3:
            self.settings_content.setCurrentIndex(3)
            self.detect_setting_widget.setup_detect_setting(self.current_filter)
            self.button4.setChecked(True)
            self.button2.setChecked(False)
            self.button1.setChecked(False)
            self.button3.setChecked(False)


    # 얼굴 레이어
    def setup_face_layout(self):
        """얼굴 인식 필터 설정 영역 레이아웃 생성"""
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style_none_line)
        
        
        face_layout = QHBoxLayout()
        face_layout.setAlignment(Qt.AlignRight)
        
        # RegisteredFacesListWidget 초기화 및 설정
        registered_faces_list_label = QLabel("필터 등록 인물")
        registered_faces_list_label.setStyleSheet(Style.title_label_middle)
        
        self.registered_faces_list_widget = RegisteredFacesListWidget()
        
        # AvailableFacesListWidget 초기화 및 설정
        available_faces_list_label = QLabel("인물 리스트")
        available_faces_list_label.setStyleSheet(Style.title_label_middle)
        
        # Add 버튼 추가
        add_face_button = QPushButton("인물 편집")
        add_face_button.setFixedSize(90, 30)
        add_face_button.setStyleSheet(Style.mini_button_style)
        add_face_button.clicked.connect(self.open_person_face_setting_dialog)
        
        self.available_faces_list_widget = AvailableFacesListWidget()
        self.available_faces_list_widget.set_items_event(self.register_face)
        
        registered_faces_list_layout = QVBoxLayout()
        registered_faces_list_layout.addWidget(registered_faces_list_label)
        registered_faces_list_layout.addWidget(self.registered_faces_list_widget)
        
        available_faces_list_layout = QGridLayout()
        available_faces_list_layout.addWidget(available_faces_list_label, 0, 0)
        available_faces_list_layout.addWidget(add_face_button, 0, 1)
        available_faces_list_layout.addWidget(self.available_faces_list_widget, 1, 0, 1, 2)
        
        self.person_face_setting_window = PersonFaceDialog()
        self.person_face_setting_window.updateEvent.connect(self.update_person_face_setting_dialog_event)
        self.person_face_setting_window.webcam_on.connect(self.webcamOn)
        
        face_layout.addLayout(registered_faces_list_layout, 2)
        face_layout.addLayout(available_faces_list_layout, 1)
        
        frame.setLayout(face_layout)
        return frame

    # 윈도우 디스플레이 설정
    def show_filter_setting_page(self, is_show):
        """윈도우 디스플레이 결정"""
        if is_show:
            self.stacked_layout.setCurrentIndex(0)
        else:
            self.stacked_layout.setCurrentIndex(1)

            
        # 현재 필터로 창 업데이트
    def set_current_filter(self, filter_name = None):
        """현제 선택된 필터로 창 업데이트"""
        self.filter_list_widget.update_list()
        self.current_filter = filter_name
        if filter_name is None or filter_name == "":
            self.show_filter_setting_page(False)
            return
            
        filter_data = self.filter_setting_processor.get_filter(filter_name)

        if filter_data:
            print("[Log] : 선택된 필터 > ", filter_name)
            self.filter_list_widget.set_select_item(filter_name)
            self.filter_title_label.set_title(filter_name)
            self.setup_setting_page(0)
            self.show_filter_setting_page(True)
        else:
            print(f"[Log] : Filter '{filter_name}' not found")
            self.show_filter_setting_page(False)


    def register_face(self, person_id):
        """얼굴 등록 메서드"""
        self.registered_faces_list_widget.register_person_faces(person_id)
        self.registered_faces_list_widget.update_list()

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

    # 필터 이름 업데이트
    def update_filter_name(self, new_name):
        """필터 이름 변경"""
        validator = self.filter_title_label.filter_name_line_edit.validator()
        state, _, _ = validator.validate(new_name,0)
        print("update filter name:", state)
        if state == QValidator.Acceptable:
            if self.current_filter:
                if self.current_filter == new_name:
                    return
                if self.filter_setting_processor.update_filter_name(self.current_filter, new_name):
                    self.set_current_filter(new_name)
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
                    msg.setText("이미 존재하는 필터 입니다")
                    msg.setWindowTitle("경고")
                    msg.exec_()
                    self.set_current_filter(self.current_filter)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("유효하지 않은 이름입니다")
            msg.setWindowTitle("경고")
            msg.exec_()      
            self.set_current_filter(self.current_filter)


    # 페이지 리프레쉬
    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        self.set_current_filter(self.current_filter)
    
        # Close Event
    def closeEvent(self, event):
        if self.person_face_setting_window is not None:
            self.person_face_setting_window.close()

    def webcamOn(self):
        self.webcam_on.emit()
        
    def cleanup(self):
        
        pass