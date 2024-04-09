import os
import cv2
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSlider, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDragEnterEvent, QDropEvent

# 비디오 파일 정보를 관리하는 클래스
class VideoInfo:
    def __init__(self, video_path):
        self.video_path = video_path
        self.video_name = os.path.basename(video_path)
        self.video_extension = os.path.splitext(video_path)[1][1:].lower()
        self.video_size = os.path.getsize(video_path)

# 비디오 재생을 위한 스레드 클래스
class VideoPlayerThread(QThread):
    video_frame = pyqtSignal(object)  # 비디오 프레임 신호
    current_frame = pyqtSignal(int)    # 현재 프레임 신호

    def __init__(self, video_path):
        super(VideoPlayerThread, self).__init__()
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.video_frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                current_frame_num = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                self.video_frame.emit(frame)        # 비디오 프레임 신호 발생
                self.current_frame.emit(current_frame_num)  # 현재 프레임 신호 발생
            else:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                
        self.cap.release()



# PyQt5를 이용한 비디오 재생 화면 구성 클래스
class VideoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

class VideoView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()

        # 비디오 위젯 추가
        self.video_widget = QLabel(self)
        self.video_widget.setFixedSize(640, 480)
        self.video_widget.setStyleSheet("background-color: black;")
        self.video_widget.setAcceptDrops(True)  # 드롭 이벤트를 허용
        self.video_widget.dragEnterEvent = self.dragEnterEvent
        self.video_widget.dropEvent = self.dropEvent
        self.video_widget.mousePressEvent = self.openFileDialogOnClick
        self.layout.addWidget(self.video_widget)

        # 파일 탐색기 버튼
        self.file_dialog_button = QPushButton("Choose Video File")
        self.file_dialog_button.clicked.connect(self.openFileDialog)
        self.layout.addWidget(self.file_dialog_button)

        # 비디오 바 (슬라이더)
        self.video_bar = QSlider(Qt.Horizontal)
        self.video_bar.setEnabled(False)
        self.video_bar.sliderMoved.connect(self.changeVideoPosition)
        self.video_bar.sliderPressed.connect(self.pauseVideo)  # 슬라이더 클릭시 일시정지
        self.layout.addWidget(self.video_bar)

        # 현재 재생 시간 표시 레이블
        self.current_time_label = QLabel("00:00:00")
        self.layout.addWidget(self.current_time_label)

        # 버튼 레이아웃
        self.button_layout = QHBoxLayout()

        # 재생 버튼
        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.playVideo)
        self.button_layout.addWidget(self.play_button)

        # 일시정지 버튼
        self.pause_button = QPushButton("Pause")
        self.pause_button.clicked.connect(self.pauseVideo)
        self.button_layout.addWidget(self.pause_button)

        # 정지 버튼
        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stopVideo)
        self.button_layout.addWidget(self.stop_button)

        self.layout.addLayout(self.button_layout)

        self.setLayout(self.layout)

    # 파일 대화상자를 통해 비디오 파일 선택
    def openFileDialog(self):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.video_info = VideoInfo(filePath)
            self.video_thread = VideoPlayerThread(filePath)
            self.video_thread.video_frame.connect(self.updateVideoFrame)
            self.video_thread.current_frame.connect(self.updateVideoBar)
            self.video_bar.setEnabled(True)
            self.video_thread.start()

    # 비디오 프레임을 QLabel 위젯에 업데이트
    def updateVideoFrame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = rgb_frame.shape
        q_img = QImage(rgb_frame.data, w, h, w * c, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_img)
        self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height()))

        # 비디오 슬라이더의 위치 업데이트
    def updateVideoBar(self, current_frame_num):
        total_frames = self.video_thread.video_frame_count
        value = int((current_frame_num / total_frames) * 100)
        self.video_bar.setValue(value)
        
        # FPS 가져오기
        fps = self.video_thread.cap.get(cv2.CAP_PROP_FPS)
        
        # 현재 재생 시간 계산
        current_time = self.convertTime(current_frame_num, total_frames, fps)
        
        # 비디오 바 왼쪽에 현재 재생 시간 표시
        self.video_bar.setTickInterval(1)  # 틱 간격을 1로 설정
        self.video_bar.setTickPosition(QSlider.TicksBothSides)  # 틱 위치 설정
        self.video_bar.setToolTip(current_time)  # 툴팁으로 현재 시간 표시

        # 비디오 바 왼쪽에 현재 재생 시간 표시
        self.current_time_label.setText(current_time)  # 현재 시간 레이블 업데이트

    def openFileDialogOnClick(self, event):
        options = QFileDialog.Options()
        filePath, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.avi *.mkv *.flv);;All Files (*)", options=options)
        if filePath:
            self.loadVideo(filePath)


    # 드래그 이벤트 오버라이드
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    # 드롭 이벤트 오버라이드
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        if files:
            file_path = files[0]  # 첫 번째 파일만 가져옴
            self.loadVideo(file_path)

    def loadVideo(self, file_path):
        self.video_info = VideoInfo(file_path)
        self.video_thread = VideoPlayerThread(file_path)
        self.video_thread.video_frame.connect(self.updateVideoFrame)
        self.video_thread.current_frame.connect(self.updateVideoBar)
        self.video_bar.setEnabled(True)
        self.video_thread.start()

    # 비디오 재생 위치 변경
    def changeVideoPosition(self, value):
        if hasattr(self, 'video_thread'):
            total_frames = self.video_thread.video_frame_count
            target_frame = int(value / 100 * total_frames)
            self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, target_frame)

    # 비디오 재생
    def playVideo(self):
        if hasattr(self, 'video_thread'):
            if self.video_thread.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.video_thread.video_frame_count:
                self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
                self.video_bar.setValue(0)  # 슬라이더 값도 초기화
            self.video_thread.start()

    # 비디오 일시정지
    def pauseVideo(self):
        if hasattr(self, 'video_thread'):
            self.video_thread.terminate()

    # 비디오 정지
    def stopVideo(self):
        if hasattr(self, 'video_thread'):
            self.video_thread.terminate()
            self.video_thread.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # 영상의 시작 지점으로 이동
            self.video_bar.setValue(0)  # 슬라이더 값도 초기화

    def convertTime(self, frame_number, total_frames, fps):
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
