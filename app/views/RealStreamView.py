from PySide6.QtWidgets import ( 
    QWidget, QFrame, QVBoxLayout, QHBoxLayout,  QGridLayout, 
    QPushButton, QLabel, QComboBox, QScrollArea,  QSplitter, QDialog, QStackedWidget
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize
from utils import Colors, Style, Icons
from controllers import RealStreamProcessor, FilterSettingController
from views.component import (
    FilterListWidget, ShadowWidget, ObjectFilterSettngWidget, 
    MosaicSettingWidget, RegisteredFacesListWidget, ContentLabeling
)
import cv2

class RealStreamView(QWidget):
    """실시간 스트리밍 View"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_controller = FilterSettingController()
        self.streaming_processor = RealStreamProcessor()  # 실시간 영상 처리 스레드 객체 생성
        self.streaming_processor.frame_ready.connect(self.update_video)  # 프레임 수신 시 GUI 업데이트 연결
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_video)
        self.current_filter = None
        self.initUI()

    def initUI(self):
        '''GUI 초기화 메서드'''
        self.stream_main_layout = QGridLayout()  # 레이아웃 설정

        toolbar = self.setup_toolbar()
        video_widget = self.setup_video_layer()
        bottom_widget = self.setup_bottom_layer()

        self.stream_main_layout.addWidget(toolbar, 0, 0)
        self.stream_main_layout.addWidget(video_widget, 0, 1)
        self.stream_main_layout.addWidget(bottom_widget, 1, 0, 1, 2)
        
        self.stream_main_layout.setRowStretch(0, 6)  # 상단 행 스트레칭 비율
        self.stream_main_layout.setRowStretch(1, 3)  # 하단 행 스트레칭 비율

        self.setLayout(self.stream_main_layout)


    def setup_toolbar(self):
        '''툴바 설정 메서드'''
        toolbar = QWidget()  # 툴바 위젯
        toolbar.setMaximumWidth(250)  # 크기 설정
        toolbar.setStyleSheet(Style.frame_style)
        toolbar.setGraphicsEffect(Style.shadow(toolbar))
        
        # 툴바 레이아웃 설정
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setContentsMargins(0,0,0,0)
        
        # 상단 핵심 버튼 설정
        core_buttons_widget = self.setup_core_buttons()
        toolbar_layout.addWidget(core_buttons_widget)

        # 중단 설정 (웹캠 선택, 비디오 배율)
        video_options_widget = self.setup_video_options()
        toolbar_layout.addWidget(video_options_widget)

        # 하단 필터 리스트
        filter_list_layout = self.setup_filter_list()
        toolbar_layout.addWidget(filter_list_layout)

        toolbar.setLayout(toolbar_layout)
        return toolbar

    def setup_core_buttons(self):
        '''상단 핵심 버튼 설정 메서드'''
        frame = QWidget()
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        frame.setFixedHeight(70)
        
        core_buttons_layout = QHBoxLayout()

        # 실시간 영상 재생/중지 버튼
        self.play_pause_button = QPushButton()
        self.play_pause_button.setFixedSize(50, 50)
        self.play_pause_button.setStyleSheet(Style.mini_button_style)
        self.play_pause_button.setIcon(QIcon(Icons.play_button))

        self.play_pause_button.setCheckable(True)
        self.play_pause_button.clicked.connect(self.toggle_webcam)

        # 일시정지 버튼
        self.stop_button = QPushButton()
        self.stop_button.setFixedSize(50,50)
        self.stop_button.setStyleSheet(Style.mini_button_style)
        self.stop_button.setIcon(QIcon(Icons.stop_button))
        self.stop_button.clicked.connect(self.stop_webcam)

        # 새 창 버튼
        self.new_window_button = QPushButton()
        self.new_window_button.setFixedSize(50,50)
        self.new_window_button.setStyleSheet(Style.mini_button_style)
        self.new_window_button.setIcon(QIcon(Icons.clone))
        self.new_window_button.clicked.connect(self.open_new_window)

        # 상단 버튼 레이아웃 설정
        core_buttons_layout.addWidget(self.play_pause_button)
        core_buttons_layout.addWidget(self.stop_button)
        core_buttons_layout.addWidget(self.new_window_button)
        core_buttons_layout.setSpacing(10)  # 버튼 사이 간격 설정
        
        frame.setLayout(core_buttons_layout)
        return frame

    def setup_video_options(self):
        '''중단 비디오 옵션 설정 메서드'''
        frame = QWidget()
        frame.setMaximumHeight(120)
        frame.setStyleSheet(Style.frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        
        video_options_layout = QGridLayout()

        # 웹캠 선택 콤보박스
        webcam_combo_label = QLabel("Webcam")
        self.webcam_combo = QComboBox()
        self.webcam_combo.setStyleSheet(f'background-color: {Colors.base_color_03}')
        self.webcam_list = self.detect_webcams()
        self.webcam_combo.addItems(self.webcam_list)
        self.webcam_combo.currentIndexChanged.connect(self.change_webcam)

        self.refreash_webcam_button = QPushButton()
        self.refreash_webcam_button.setFixedSize(30, 30)
        self.refreash_webcam_button.setStyleSheet(Style.mini_button_style)
        self.refreash_webcam_button.setIcon(QIcon(Icons.reload))
        self.refreash_webcam_button.clicked.connect(self.refreash_webcam_combox())        

        # 중단 레이아웃 설정
        video_options_layout.addWidget(webcam_combo_label, 0, 0)
        video_options_layout.addWidget(self.webcam_combo, 1, 0)
        video_options_layout.addWidget(self.refreash_webcam_button, 1, 1)
        
        frame.setLayout(video_options_layout)
        return frame

    def setup_filter_list(self):
        '''필터 리스트 위젯'''
        # Filter 목록
        frame = QWidget()
        frame.setStyleSheet(Style.list_frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        layout = QVBoxLayout()
        
        list_label = QLabel("필터 목록")
        list_label.setStyleSheet(Style.list_frame_label)
        
        self.filter_list_widget = FilterListWidget()
        self.filter_list_widget.set_items_event(self.set_current_filter)
        
        layout.addWidget(list_label)
        layout.addWidget(self.filter_list_widget)
        frame.setLayout(layout)

        return frame

    def setup_video_layer(self):
        '''비디오 레이어 설정 메서드'''
        frame = QFrame()
        video_layout = QHBoxLayout()
        
        self.video_box = QLabel()  # 비디오 플레이어 레이블
        self.video_box.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 및 테두리 설정
        self.video_box.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 정렬 설정
        video_layout.addWidget(self.video_box)
        self.video_box.setFixedWidth(725)
        frame.setLayout(video_layout)

        self.cam_dialog = QDialog()
        layer = QGridLayout()
        layer.setContentsMargins(0,0,0,0)
        self.dialog_videolable = QLabel()
        self.dialog_videolable.setStyleSheet(f'background-color: {Colors.baseColor01};')  # 배경색 및 테두리 설정
        self.dialog_videolable.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)  # 정렬 설정
        layer.addWidget(self.dialog_videolable)
        self.cam_dialog.setLayout(layer)

        return frame
        

    def setup_bottom_layer(self):
        '''하단 레이어 설정 메서드'''
        frame = QWidget()  # 하단 위젯
        frame.setStyleSheet(Style.frame_style)  # 배경색 및 테두리 설정
        frame.setGraphicsEffect(Style.shadow(frame))
        
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        # 각각의 위젯 생성
        self.setting_01 = RegisteredFacesListWidget()
        self.setting_01.onEventUpdate.connect(self.update_filter)
        self.setting_02 = ObjectFilterSettngWidget()
        self.setting_02.onEventUpdate.connect(self.update_filter)
        self.setting_03 = MosaicSettingWidget()
        self.setting_03.onEventUpdate.connect(self.update_filter)
        
        self.widget1 = ContentLabeling()
        self.widget1.setLabel("필터링 인물 관리")
        self.widget1.setContent(self.setting_01)
        
        self.widget2 = ContentLabeling()
        self.widget2.setLabel("유해 매체 필터링")
        self.widget2.setContent(self.setting_02)
        
        self.widget3 = ContentLabeling()
        self.widget3.setLabel("모자이크 블러 설정")
        self.widget3.setContent(self.setting_03)
        

        # 스플리터 생성 및 각 위젯 추가
        splitter = QSplitter()
        splitter.addWidget(self.widget1)
        splitter.addWidget(self.widget2)
        splitter.addWidget(self.widget3)
        splitter.setSizes([300, 200, 200])  # 초기 비율을 3:2:2로 설정

        self.stackedWidget = QStackedWidget()
        self.empty = QWidget()
        self.stackedWidget.addWidget(self.empty)
        self.stackedWidget.addWidget(splitter)

        # 레이아웃 설정
        layout = QHBoxLayout()
        layout.addWidget(self.stackedWidget)
        frame.setLayout(layout)
        return frame
    
    def show_setting(self, show):
        if show:
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.stackedWidget.setCurrentIndex(0)


    def setup_settings(self, filter_name):
        """세팅 셋업"""
        if filter_name is not None:
            self.setting_01.set_filter(filter_name)
            self.setting_01.update_list()
            self.setting_02.setup_object_filter_widget(filter_name)
            self.setting_03.setup_mosaic_setting(filter_name)


    # method
    def toggle_webcam(self):
        '''웹캠 토글 메서드'''
        if self.play_pause_button.isChecked():
            if not self.streaming_processor.isRunning():
                self.streaming_processor.start()
                self.play_pause_button.setIcon(QIcon(Icons.play_button))
                self.timer.start(0)  # 비동기적으로 프레임 업데이트
        else:
            if self.streaming_processor.isRunning():
                self.play_pause_button.setIcon(QIcon(Icons.puse_button))
                self.streaming_processor.pause()
                self.timer.stop()
                
    def stop_webcam(self):
        '''웹캠 정지 메서드'''
        # todo : 웹 캠 정지 -> 녹화기능으로 변경
        raise NotImplementedError("This function is not implemented yet")
    
    def open_new_window(self):
        '''새창 메서드'''
        self.cam_dialog.show()
        # 웹캠 새장 로직 추가
    
    def change_webcam(self, index):
        '''웹캠 변경 메서드'''
        self.streaming_processor.set_web_cam(index)

    def set_current_filter(self, filter_name = None):
        '''필터 옵션 선택'''
        if filter_name is not None and self.filter_controller.get_filter(filter_name):
            print("[Log] : 선택된 필터 > ", filter_name)
            self.current_filter = filter_name
            self.streaming_processor.set_filter(filter_name)
            self.show_setting(True)
            self.setup_settings(filter_name)
        else:
            print("[Log] : 필터 미선택")
            self.streaming_processor.set_filter(None)
            self.show_setting(False)
            
    def update_filter(self):
        if self.current_filter:
            self.streaming_processor.set_filter(self.current_filter)
        
    def update_video(self, q_img=None):
        '''비디오 업데이트 메서드'''
        if q_img is None:
            return
        pixmap = QPixmap.fromImage(q_img)
        self.video_box.setPixmap(pixmap.scaled(self.video_box.width(), self.video_box.height(), Qt.KeepAspectRatio))
        self.dialog_videolable.setPixmap(pixmap.scaled(self.video_box.width(), self.video_box.height(), Qt.KeepAspectRatio))
    
    def detect_webcams(self):
        # 연결된 카메라 장치를 검색합니다.
        index = 0
        name_list = list()
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            
            # 장치의 이름을 가져옵니다.
            name_list.append(str(index))
            cap.release()
            index += 1
        
        return name_list
    
    def refreash_webcam_combox(self):
        namelist = self.detect_webcams()
        combox = QComboBox()
        combox.addItems(namelist)
        self.webcam_combo = combox
        self.webcam_combo.currentIndexChanged.connect(self.change_webcam)

    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        self.set_current_filter(self.current_filter)

    def closeEvent(self, event):
        '''GUI 종료 이벤트 메서드'''
        self.streaming_processor.stop()
        self.streaming_processor.wait()
        self.timer.stop()
        del self.streaming_processor
        del self.timer
