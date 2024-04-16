import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent
from controllers import VideoProcessor

class VideoInfo:
    '''비디오 파일 정보를 관리하는 클래스'''
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_name = os.path.basename(video_path)
        self.video_extension = os.path.splitext(video_path)[1][1:].lower()
        self.video_size = os.path.getsize(video_path)


class VideoProcessor(QThread):
    '''비디오 재생을 위한 스레드 클래스'''
    video_frame = pyqtSignal(object)  # 비디오 프레임 신호
    current_frame = pyqtSignal(int)    # 현재 프레임 신호
    fps_signal = pyqtSignal(float)     # FPS 신호

    def __init__(self, video_path):
        super(VideoProcessor, self).__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))  # FPS 값 가져오기
        self.is_playing = True

    def run(self):
        '''비디오 재생 스레드의 메인 루프'''
        while self.cap.isOpened() and self.is_playing:
            ret, frame = self.cap.read()
            if ret:
                current_frame_num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.video_frame.emit(frame)        # 비디오 프레임 신호 발생
                self.current_frame.emit(current_frame_num)  # 현재 프레임 신호 발생
                self.fps_signal.emit(self.fps)      # FPS 신호 발생
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                
        self.cap.release()



class VideoView(QWidget):
    '''PyQt5를 이용한 비디오 재생 화면 구성 클래스'''
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        '''UI 초기화'''
        self.layout = QVBoxLayout()

        # 비디오 위젯 추가
        self.video_widget = QLabel(self)
        self.video_widget.setScaledContents(True)  # 이미지 비율 유지
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_widget.setAcceptDrops(True)  # 드롭 이벤트를 허용
        self.video_widget.dragEnterEvent = self.dragEnterEvent
        self.video_widget.dropEvent = self.dropEvent
        self.video_widget.mousePressEvent = self.openFileDialogOnClick

        # QLabel을 수직 레이아웃에 추가
        self.layout.addWidget(self.video_widget)

        # 파일 탐색기 버튼
        self.file_dialog_button = QPushButton("Choose Video File")
        self.file_dialog_button.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.file_dialog_button)

        # 비디오 바 (슬라이더), 현재 재생 시간, FPS 정보를 위한 레이아웃
        self.bottom_layout = QHBoxLayout()

        # 재생, 일시정지, 정지 버튼
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.playVideo)
        self.bottom_layout.addWidget(self.play_button)

        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pauseVideo)
        self.bottom_layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopVideo)
        self.bottom_layout.addWidget(self.stop_button)

        # 비디오 바
        self.video_bar = QSlider(Qt.Horizontal)
        self.video_bar.setEnabled(False)
        self.video_bar.sliderMoved.connect(self.changeVideoPosition)
        self.video_bar.sliderPressed.connect(self.pauseVideo)
        self.bottom_layout.addWidget(self.video_bar)

        # 현재 재생 시간 표시 레이블
        self.current_time_label = QLabel("00:00:00")
        self.bottom_layout.addWidget(self.current_time_label)

        # FPS 값을 표시하는 레이블
        self.fps_label = QLabel("FPS: --")
        self.bottom_layout.addWidget(self.fps_label)

        self.layout.addLayout(self.bottom_layout)

        self.setLayout(self.layout)
        

    def resizeEvent(self, event):
        '''부모 레이아웃의 크기가 변경될 때마다 비디오 위젯의 크기를 조정'''
        super().resizeEvent(event)
        parent_width = self.width()
        parent_height = self.height()

        # 가로 길이를 부모 레이아웃 크기에 맞추기
        self.video_widget.setFixedWidth(parent_width)

        # 가로 길이의 16:9 비율로 높이 설정
        video_height = int(parent_width / 16 * 9)
        self.video_widget.setFixedHeight(video_height)


    def openFileDialog(self):
        '''파일 대화상자를 통해 비디오 파일 선택'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.video_info = VideoInfo(filePath)
            self.video_thread = VideoProcessor(filePath)
            self.video_thread.video_frame.connect(self.updateVideoFrame)
            self.video_thread.current_frame.connect(self.updateVideoBar)
            self.video_thread.fps_signal.connect(self.updateFPSLabel)  # FPS 신호 연결
            self.video_bar.setEnabled(True)
            self.video_thread.start()


    def updateVideoFrame(self, frame):
        '''비디오 프레임을 QLabel 위젯에 업데이트'''
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_frame.shape
        q_img = QImage(rgb_frame.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height()))


    def updateVideoBar(self, current_frame_num):
        '''비디오 슬라이더의 위치 업데이트'''
        total_frames = self.video_thread.video_frame_count
        value = int((current_frame_num / total_frames) * 100)
        self.video_bar.setValue(value)
        
        # FPS 가져오기
        fps = self.video_thread.fps
        current_time = self.convertTime(current_frame_num, total_frames, fps)
        
        # 비디오 바 왼쪽에 현재 재생 시간 표시
        self.video_bar.setTickInterval(1)  # 틱 간격을 1로 설정
        self.video_bar.setTickPosition(QSlider.TicksBothSides)  # 틱 위치 설정
        self.video_bar.setToolTip(current_time)  # 툴팁으로 현재 시간 표시

        # 현재 재생 시간 레이블 업데이트
        self.current_time_label.setText(current_time)


    def updateFPSLabel(self, fps_value):
        '''FPS 레이블 업데이트'''
        self.fps_label.setText(f"FPS: {fps_value}")


    def openFileDialogOnClick(self, event):
        '''파일 대화상자를 통해 비디오 파일 선택 (마우스 클릭 이벤트로 트리거)'''
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.loadVideo(filePath)


    def dragEnterEvent(self, event: QDragEnterEvent):
        '''드래그 이벤트 오버라이드'''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()


    def dropEvent(self, event: QDropEvent):
        '''드롭 이벤트 오버라이드'''
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            file_path = files[0]  # 첫 번째 파일만 가져옴
            self.loadVideo(file_path)


    def loadVideo(self, file_path):
        '''비디오 파일 로드'''
        self.video_info = VideoInfo(file_path)
        self.video_thread = VideoProcessor(file_path)
        self.video_thread.video_frame.connect(self.updateVideoFrame)
        self.video_thread.current_frame.connect(self.updateVideoBar)
        self.video_bar.setEnabled(True)
        self.video_thread.start()


    def changeVideoPosition(self, value):
        '''비디오 재생 위치 변경'''
        if hasattr(self, 'video_thread'):
            total_frames = self.video_thread.video_frame_count
            target_frame = int(value / 100 * total_frames)
            self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)


    def playVideo(self):
        '''비디오 재생'''
        if hasattr(self, 'video_thread'):
            if self.video_thread.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.video_thread.video_frame_count:
                self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
                self.video_bar.setValue(0)  # 슬라이더 값도 초기화
            self.video_thread.start()


    def pauseVideo(self):
        '''비디오 일시정지'''
        if hasattr(self, 'video_thread'):
            self.video_thread.terminate()


    def stopVideo(self):
        '''비디오 정지'''
        if hasattr(self, 'video_thread'):
            self.video_thread.terminate()
            self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
            self.video_bar.setValue(0)  # 슬라이더 값도 초기화


    def convertTime(self, frame_number, total_frames, fps):
        '''프레임 번호를 시간 형식으로 변환'''
        if fps == 0:
            return "00:00:00"  # fps 값이 0일 경우 "00:00:00"을 반환하여 오류를 방지
        seconds = frame_number / fps
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = VideoView()
    window.show()
    sys.exit(app.exec_())
