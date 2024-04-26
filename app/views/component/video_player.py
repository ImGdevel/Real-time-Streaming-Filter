import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSlider, QFrame, QHBoxLayout, QLabel
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon


class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")

        self.media_player = QMediaPlayer()
        self.video_widget = QVideoWidget()        
        self.video_widget.setMaximumHeight(768)
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
        
        self.setAcceptDrops(True)


    def set_video(self, video_path):
        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        
    def set_current_time(self, time):
        self.current_time_label.setText(time)

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

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        print("드랍!")
        for url in event.mimeData().urls():
            path = url.toLocalFile()
            if path.endswith(('.mp4', '.avi', '.mov')):
                self.set_video(path)
                break
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_player = VideoPlayer()
    video_player.show()
    sys.exit(app.exec())