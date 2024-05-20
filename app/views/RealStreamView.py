from PySide6.QtWidgets import ( 
    QWidget, QFrame, QVBoxLayout, QHBoxLayout,  QGridLayout, 
    QPushButton, QLabel, QComboBox, QScrollArea,  QSplitter, QDialog, 
    QStackedWidget, QButtonGroup, QMessageBox
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from utils import Colors, Style, Icons
from controllers import RealStreamProcessor, FilterSettingController
from views.component import (
    FilterListWidget, ObjectFilterSettngWidget, 
    BlurSettingWidget, RegisteredFacesListWidget, ContentLabeling, CamWindow,
    DetectSettingWidget, StreamVideoPlayer
)
import cv2

class RealStreamView(QWidget):
    webcam_on = Signal()
    """실시간 스트리밍 View"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_controller = FilterSettingController()
        self.stream_video_player = StreamVideoPlayer()
        self.streaming_processor = RealStreamProcessor()  # 실시간 영상 처리 스레드 객체 생성
        self.streaming_processor.frame_ready.connect(self.stream_video_player.update_video)  # 프레임 수신 시 GUI 업데이트 연결
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.stream_video_player.update_video)
        self.current_filter = None
        self.cam_dialog = None
        # self.original_size : QSize = None
        # self.current_size : QSize = None
        self.initUI()

    def initUI(self):
        '''GUI 초기화 메서드'''
        stream_main_layout = QGridLayout()  # 레이아웃 설정

        toolbar = self.setup_toolbar()
        video_widget = self.setup_video_layer()
        bottom_widget = self.setup_bottom_layer()

        stream_main_layout.addWidget(toolbar, 0, 0)
        stream_main_layout.addWidget(video_widget, 0, 1)
        stream_main_layout.addWidget(bottom_widget, 1, 0, 1, 2)
        
        stream_main_layout.setRowStretch(0, 7)  # 상단 행 스트레칭 비율
        stream_main_layout.setRowStretch(1, 3)  # 하단 행 스트레칭 비율

        self.setLayout(stream_main_layout)


    def setup_toolbar(self):
        '''툴바 설정 메서드'''
        toolbar = QWidget()  # 툴바 위젯
        toolbar.setMaximumWidth(250)  # 크기 설정
        toolbar.setStyleSheet(Style.frame_style_background)
        toolbar.setGraphicsEffect(Style.shadow(toolbar))
        
        # 툴바 레이아웃 설정
        toolbar_layout = QVBoxLayout()
        toolbar_layout.setContentsMargins(0,0,0,0)
        
        # 상단 핵심 버튼 설정
        core_buttons_widget = self.setup_core_buttons()
    
        # 중단 설정 (웹캠 선택, 비디오 배율)
        video_options_widget = self.setup_video_options()
    
        # 하단 필터 리스트
        filter_list_layout = self.setup_filter_list()
        
        toolbar_layout.addWidget(core_buttons_widget)
        toolbar_layout.addWidget(video_options_widget)
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
        self.play_pause_button.setToolTip("실시간 스트리밍 시작")
        self.play_pause_button.setCheckable(True)
        self.play_pause_button.clicked.connect(self.toggle_webcam)

        # 녹화 버튼
        self.recode_button = QPushButton()
        self.recode_button.setFixedSize(50, 50)
        self.recode_button.setStyleSheet(Style.mini_button_style)
        self.recode_button.setToolTip("화면 녹화 시작")
        self.recode_button.setIcon(QIcon(Icons.recode))
        self.recode_button.setCheckable(True)
        self.recode_button.clicked.connect(self.record_video)
        

        # 새 창 버튼
        self.new_window_button = QPushButton()
        self.new_window_button.setFixedSize(50, 50)
        self.new_window_button.setStyleSheet(Style.mini_button_style)
        self.new_window_button.setToolTip("새 창")
        self.new_window_button.setIcon(QIcon(Icons.browser))
        self.new_window_button.clicked.connect(self.open_new_window)
        
        # 상단 버튼 레이아웃 설정
        core_buttons_layout.addWidget(self.play_pause_button)
        core_buttons_layout.addWidget(self.recode_button)
        core_buttons_layout.addWidget(self.new_window_button)
        core_buttons_layout.setSpacing(10)  # 버튼 사이 간격 설정
        
        frame.setLayout(core_buttons_layout)
        return frame

    def setup_video_options(self):
        '''중단 비디오 옵션 설정 메서드'''
        frame = QWidget()
        frame.setFixedHeight(100)
        frame.setGraphicsEffect(Style.shadow(frame))
        
        video_options_layout = QVBoxLayout()
        video_options_layout.setAlignment(Qt.AlignTop)
        video_options_layout.setContentsMargins(0,0,0,0)
        video_options_layout.setSpacing(0)
        
        button_layout_frame = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        button_layout.setSpacing(0)
        button_layout.setAlignment(Qt.AlignLeft)
        
        # 웹캠 선택 콤보박스
        self.webcam_button = QPushButton("웹 캠")
        self.webcam_button.setFixedSize(80,30)
        self.webcam_button.setStyleSheet(Style.cam_button_selected)
        self.webcam_button.clicked.connect(lambda: self.select_video_option(0))
        
        self.screen_button = QPushButton("화면 캡쳐")
        self.screen_button.setFixedSize(80,30)
        self.screen_button.setStyleSheet(Style.cam_button)
        self.screen_button.clicked.connect(lambda: self.select_video_option(1))

        self.screen_focus_button = QPushButton("집중 탐색")
        self.screen_focus_button.setFixedSize(80,30)
        self.screen_focus_button.setStyleSheet(Style.cam_button)
        self.screen_focus_button.clicked.connect(lambda: self.select_video_option(2))
    
        button_layout.addWidget(self.webcam_button)
        button_layout.addWidget(self.screen_button)
        button_layout.addWidget(self.screen_focus_button)
        button_layout_frame.setLayout(button_layout)
        
        # 웹캠 선택시 내용 출력
        webcam_content_widget = QWidget()
        webcam_content_laytout = QHBoxLayout()
        webcam_content_laytout.setContentsMargins(20,10,20,10)
        
        self.webcam_combo = QComboBox()
        self.webcam_combo.setStyleSheet(f'background-color: {Colors.base_color_03}')
        self.webcam_list = self.detect_webcams()
        self.webcam_combo.addItems(self.webcam_list)
        self.webcam_combo.currentIndexChanged.connect(self.change_webcam)

        self.refreash_webcam_button = QPushButton()
        self.refreash_webcam_button.setFixedSize(30, 30)
        self.refreash_webcam_button.setStyleSheet(Style.mini_button_style)
        self.refreash_webcam_button.setIcon(QIcon(Icons.reload))
        self.refreash_webcam_button.setToolTip('새로고침')
        self.refreash_webcam_button.clicked.connect(self.refresh_webcam_combox)
        
        webcam_content_laytout.addWidget(self.webcam_combo)
        webcam_content_laytout.addWidget(self.refreash_webcam_button)
        webcam_content_widget.setLayout(webcam_content_laytout)
        
        #화면 캡쳐시 내용 출력
        screen_capture_content_widget = QWidget()
        screen_capture_content_layout = QHBoxLayout()
        screen_capture_content_layout.setSpacing(10)
        
        self.screen_capture_button = QPushButton()
        self.screen_capture_button.setFixedSize(40, 40)
        self.screen_capture_button.setStyleSheet(Style.mini_button_style)
        self.screen_capture_button.setIcon(QIcon(Icons.screen_desktop))
        self.screen_capture_button.setToolTip('영역 선택')
        self.screen_capture_button.clicked.connect(self.set_screen_capture_area)
        
        self.screen_size_label = QLabel("screen : ")
        self.screen_size_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.streaming_processor.screen_size.connect(self.set_screen_size)
        
        screen_capture_content_layout.addWidget(self.screen_capture_button, 1)
        screen_capture_content_layout.addWidget(self.screen_size_label, 6)
        screen_capture_content_widget.setLayout(screen_capture_content_layout)

        #집중 탐색 구역 설정
        screen_focus_area_widget = QWidget()
        screen_focus_area_layout = QHBoxLayout()
        screen_focus_area_layout.setSpacing(10)

        self.focus_area_capture_button = QPushButton()
        self.focus_area_capture_button.setFixedSize(40, 40)
        self.focus_area_capture_button.setStyleSheet(Style.mini_button_style)
        self.focus_area_capture_button.setIcon(QIcon(Icons.screen_desktop))
        self.focus_area_capture_button.setToolTip('영역 선택')
        self.focus_area_capture_button.clicked.connect(self.set_focus_area_size)

        screen_focus_area_layout.addWidget(self.focus_area_capture_button,1)
        screen_focus_area_widget.setLayout(screen_focus_area_layout)

        # 위젯 전환
        self.video_options_content = QStackedWidget()
        self.video_options_content.setStyleSheet(Style.frame_style)
        self.video_options_content.addWidget(webcam_content_widget)
        self.video_options_content.addWidget(screen_capture_content_widget)
        self.video_options_content.addWidget(screen_focus_area_widget)
        
        
        video_options_layout.addWidget(button_layout_frame)
        video_options_layout.addWidget(self.video_options_content)
        
        frame.setLayout(video_options_layout)
        return frame

    def setup_filter_list(self):
        '''필터 리스트 위젯'''
        # Filter 목록
        frame = QWidget()
        frame.setStyleSheet(Style.list_frame_style)
        frame.setGraphicsEffect(Style.shadow(frame))
        layout = QVBoxLayout()
        layout.setContentsMargins(20,10,20,10)
        
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
        video = self.stream_video_player
        
        return video
        

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
        self.setting_03 = BlurSettingWidget()
        self.setting_03.onEventUpdate.connect(self.update_filter)
        self.setting_04 = DetectSettingWidget()
        self.setting_04.onEventUpdate.connect(self.update_filter)
        
        self.widget1 = ContentLabeling()
        self.widget1.setLabel("필터링 인물 관리")
        self.widget1.setContent(self.setting_01)
        
        self.widget2 = ContentLabeling()
        self.widget2.setLabel("유해 매체 필터링")
        self.widget2.setContent(self.setting_02)
        
        self.widget3 = ContentLabeling()
        self.widget3.setLabel("모자이크 블러 설정")
        self.widget3.setContent(self.setting_03)
        
        self.widget4 = ContentLabeling()
        self.widget4.setLabel("감지 정확도 설정")
        self.widget4.setContent(self.setting_04)
        

        # 스플리터 생성 및 각 위젯 추가
        splitter = QSplitter()
        splitter.addWidget(self.widget1)
        splitter.addWidget(self.widget2)
        splitter.addWidget(self.widget3)
        splitter.addWidget(self.widget4)
        splitter.setSizes([300, 200, 200, 200])

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
            self.setting_04.setup_detect_setting(filter_name)


    # method
    def toggle_webcam(self):
        '''웹캠 토글 메서드'''
        if not self.streaming_processor.is_running:
            self.start_streaming()
        else:
            self.stop_streaming()
    
    def start_streaming(self):
        self.play_pause_button.setIcon(QIcon(Icons.puse_button))
        self.play_pause_button.setToolTip("실시간 스트리밍 중지")
        self.streaming_processor.start()
        self.timer.start(0)  # 비동기적으로 프레임 업데이트
            
    def stop_streaming(self):
        self.play_pause_button.setIcon(QIcon(Icons.play_button))
        self.play_pause_button.setToolTip("실시간 스트리밍 시작")
        self.streaming_processor.pause()
        if self.recode_button.isChecked():
            self.recode_button.setChecked(False)
            self.streaming_processor.recordOff()
            self.recode_button.setStyleSheet(Style.mini_button_style)
        self.timer.stop()
        
        
            
    def set_screen_capture_area(self):
        '''화면 캡쳐 녹화'''
        if self.streaming_processor.isRunning():
            self.stop_streaming()
            if self.streaming_processor.capture_mode == 0:
                self.streaming_processor.stop()
        self.play_pause_button.setChecked(False)
        self.streaming_processor.set_capture_area()
                
    def record_video(self):
        '''웹캠 정지 메서드'''
        # todo : 웹 캠 정지 -> 녹화기능으로 변경
        try:
            print(self.recode_button.isChecked())
            
            if self.recode_button.isChecked():
                self.recode_button.setChecked(True)
                self.streaming_processor.recordOn()
                self.recode_button.setStyleSheet(Style.mini_button_style_seletecd)
            else:
                self.recode_button.setChecked(False)
                self.streaming_processor.recordOff()
                self.recode_button.setStyleSheet(Style.mini_button_style)
            
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("실시간 스트리밍 촬영이 시작되지 않아 녹화를 진행할 수 없습니다")
            msg.setWindowTitle("경고")
            msg.exec_()
            self.recode_button.setChecked(False)
    
    def stop_webcam(self):
        if self.streaming_processor.isRunning():
            self.stop_streaming()
        self.streaming_processor.stop()
        self.play_pause_button.setChecked(False)
    
    def open_new_window(self):
        '''새창 메서드'''
        self.cam_dialog = CamWindow()
        self.streaming_processor.frame_ready.connect(self.cam_dialog.update_frame)
        self.cam_dialog.show()
    
    def change_webcam(self, index):
        '''웹캠 변경 메서드'''
        self.streaming_processor.set_web_cam(index)

    def set_current_filter(self, filter_name = None):
        '''필터 옵션 선택'''
        if filter_name is not None and self.filter_controller.get_filter(filter_name):
            print("[Log] : 선택된 필터 > ", filter_name)
            self.current_filter = filter_name
            self.streaming_processor.set_filter(filter_name)
            self.filter_list_widget.set_select_item(filter_name)
            self.show_setting(True)
            self.setup_settings(filter_name)
        else:
            print("[Log] : 필터 미선택")
            self.current_filter = None
            self.streaming_processor.set_filter(None)
            self.show_setting(False)
            
    def update_filter(self):
        if self.current_filter:
            self.streaming_processor.set_filter(self.current_filter)
        
    def update_video(self, q_img=None):
        '''비디오 업데이트 메서드'''
        if q_img is None:
            return
        if self.original_size is None:
            self.original_size = q_img.size()
            print(self.original_size)
        
        pixmap = QPixmap.fromImage(q_img)
        self.video_box.setPixmap(pixmap.scaled(self.video_box.width(), self.video_box.height(), Qt.KeepAspectRatio))
        if self.current_size is None :
            self.current_size = QSize(self.video_box.width(), self.video_box.height())
        elif self.current_size.width() != self.video_box.width() or self.current_size.height() != self.video_box.height(): 
            self.current_size = QSize(self.video_box.width(), self.video_box.height())
    
    def select_video_option(self, index):
        if index == 0:  # 웹캠 선택
            self.webcam_button.setStyleSheet(Style.cam_button_selected)
            self.screen_button.setStyleSheet(Style.cam_button)
            self.screen_focus_button.setStyleSheet(Style.cam_button)
            self.video_options_content.setCurrentIndex(0)
        elif index == 1:  # 화면 캡쳐 선택
            self.screen_button.setStyleSheet(Style.cam_button_selected)
            self.webcam_button.setStyleSheet(Style.cam_button)
            self.screen_focus_button.setStyleSheet(Style.cam_button)
            self.video_options_content.setCurrentIndex(1)
        elif index == 2:
            self.screen_button.setStyleSheet(Style.cam_button)
            self.webcam_button.setStyleSheet(Style.cam_button)
            self.screen_focus_button.setStyleSheet(Style.cam_button_selected)
            self.video_options_content.setCurrentIndex(2)
            
    
    def set_screen_size(self, size : str):
        """스크린 사이즈 텍스트"""
        screen_size = "screen : " + str(size[0]) + "x" + str(size[1])
        self.screen_size_label.setText(screen_size)
    
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
    
    def refresh_webcam_combox(self):
        print("refresh")
        self.running_webcam_stop()
        namelist = self.detect_webcams()
        combox = QComboBox()
        combox.addItems(namelist)
        self.webcam_combo = combox
        self.streaming_processor.set_webcam_mode()


    def render(self):
        """페이지 refesh"""
        self.filter_list_widget.update_list()
        self.set_current_filter(self.current_filter)

    def closeEvent(self, event):
        '''GUI 종료 이벤트 메서드'''
        self.streaming_processor.stop()
        #self.streaming_processor.wait()
        self.timer.stop()
        del self.streaming_processor
        del self.timer
        if self.cam_dialog is not None:
            self.cam_dialog.close()

    def running_webcam_stop(self):
        if self.streaming_processor.isRunning():
            self.stop_streaming()
            if self.streaming_processor.capture_mode == 0:
                self.streaming_processor.stop()
        else:
            if self.streaming_processor.capture_mode == 0:
                if self.streaming_processor.webcam_on:
                    self.streaming_processor.stop()
        self.play_pause_button.setChecked(False)
        
    def swap_event(self):
        self.stop_streaming()
        
    def set_focus_area_size(self):
        if self.streaming_processor.is_running is True:
            self.stream_video_player.focusSelectMode = not self.stream_video_player.focusSelectMode
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("실시간 스트리밍 촬영이 시작되지 않아 집중 탐색구역을 설정할 수 없습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
    
