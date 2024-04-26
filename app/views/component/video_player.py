import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QFrame, QHBoxLayout, QLabel
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtGui import QIcon, QDragEnterEvent, QDropEvent
from PySide6.QtCore import QUrl, Qt, Signal

class VideoPlayer(QWidget):
    setPlayVideo = Signal(str)
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()        
        self.video_widget.setMaximumHeight(768)
        self.setAcceptDrops(True)
        self.video_widget.dragEnterEvent = self.dragEnterEvent
        self.video_widget.dropEvent = self.dropEvent
        
        
        self.video_player_bar_layout = QHBoxLayout()
        

        self.start_button = QPushButton()
        self.start_button.setFixedSize(30,30)
        self.start_button.setIcon(QIcon('./resources/icons/cil-media-play.png'))
        self.start_button.clicked.connect(self.start_video)

        self.pause_button = QPushButton()
        self.pause_button.setFixedSize(30,30)
        self.pause_button.setIcon(QIcon('./resources/icons/cil-media-pause.png'))
        self.pause_button.clicked.connect(self.pause_video)

        self.stop_button = QPushButton()
        self.stop_button.setFixedSize(30,30)
        self.stop_button.setIcon(QIcon('./resources/icons/cil-media-stop.png'))
        self.stop_button.clicked.connect(self.stop_video)
    
        
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.sliderMoved.connect(self.set_position)
        
        self.current_time_label = QLabel("00:00:00")

        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        
        self.video_player_bar_layout.addWidget(self.start_button)
        self.video_player_bar_layout.addWidget(self.pause_button)
        self.video_player_bar_layout.addWidget(self.stop_button)
        self.video_player_bar_layout.addWidget(self.current_time_label)
        self.video_player_bar_layout.addWidget(self.slider)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addLayout(self.video_player_bar_layout)
        self.setLayout(layout)
        
    
    def set_video(self, video_path):
        self.media_player.setSource(QUrl.fromLocalFile(video_path))

    def start_video(self):
        self.media_player.play()

    def pause_video(self):
        self.media_player.pause()

    def stop_video(self):
        self.media_player.stop()

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.slider.setValue(position)
        self.set_current_time(position)

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        
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
            self.set_video(file_path)
            self.setPlayVideo.emit(file_path)
            
    def set_current_time(self, time):
        time_text = self.convertTime(time)
        self.current_time_label.setText(time_text)
            
    def convertTime(self, time):
        '''프레임 번호를 시간 형식으로 변환'''
        seconds = time / 1000
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())