import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import time

class WorkerThread(QThread):
    progress_update = pyqtSignal(int)

    def run(self):
        for i in range(101):
            time.sleep(0.1)
            self.progress_update.emit(i)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("로딩 스피너 예제")
        layout = QVBoxLayout()

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # 원형 스피너로 설정
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("작업 시작")
        self.start_button.clicked.connect(self.start_loading)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

        self.worker_thread = WorkerThread()
        self.worker_thread.progress_update.connect(self.update_progress)

    def start_loading(self):
        self.progress_bar.setValue(0)
        self.worker_thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
