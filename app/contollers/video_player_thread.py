import cv2
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QImage, QPixmap

class VideoPlayerThread(QThread):
    def __init__(self, video_path, video_widget):
        super().__init__()
        self.video_path = video_path
        self.video_widget = video_widget

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = rgb_frame.shape
                q_img = QImage(rgb_frame.data, w, h, w * c, QImage.Format_RGB888)
                pixmap = QPixmap.fromImage(q_img)
                self.video_widget.setPixmap(pixmap.scaled(self.video_widget.width(), self.video_widget.height()))
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
