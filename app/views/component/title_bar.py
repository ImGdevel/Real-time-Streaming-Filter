from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget
from PySide6.QtCore import Qt, QPoint, QEvent
from utils import Colors, Style

class TitleBar(QWidget):

    def __init__(self, parent):
        super(TitleBar, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        """TitleBar UI 초기화 메서드"""
        # 수평 레이아웃 초기화
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignVCenter)

        # 타이틀 라벨 설정
        self.title = QLabel("")
        self.title.setFixedHeight(40)
        self.title.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.title.setStyleSheet(Style.title_bar_style)

        # 버튼 설정 및 스타일 적용
        self.btn_close = self.createButton("x", self.btn_close_clicked, 25)
        self.btn_min = self.createButton("-", self.btn_min_clicked, 25)

        # 레이아웃에 위젯 추가
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_close)

        self.setLayout(self.layout)
        
        # 마우스 이벤트 처리를 위한 변수 초기화
        self.start = QPoint(0, 0)
        self.pressing = False

    def createButton(self, text, clicked, size):
        """버튼 생성 및 스타일 적용 메서드"""
        button = QPushButton(text)
        button.clicked.connect(clicked)
        button.setFixedSize(size, size)
        button.setStyleSheet(Style.title_bar_button)
        return button
    
    def set_title(self, text):
        """타이틀바 이름 변경"""
        self.title.setText(text)

    def hex_to_rgb(self, color):
        """Hex color를 RGB 튜플로 변환하는 함수"""
        color = color.lstrip('#')
        return tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    def resizeEvent(self, event: QEvent.Resize):
        """위젯 크기 변경 이벤트 핸들러"""
        super(TitleBar, self).resizeEvent(event)
        self.title.setFixedWidth(self.parent.width())

    def mousePressEvent(self, event: QEvent.MouseButtonPress):
        """마우스 클릭 이벤트 핸들러"""
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event: QEvent.MouseMove):
        """마우스 드래그 이벤트 핸들러"""
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end - self.start
            self.parent.setGeometry(
                self.mapToGlobal(self.movement).x(),
                self.mapToGlobal(self.movement).y(),
                self.parent.width(),
                self.parent.height()
            )
            self.start = self.end

    def mouseReleaseEvent(self, event: QEvent.MouseButtonRelease):
        """마우스 클릭 해제 이벤트 핸들러"""
        self.pressing = False

    def btn_close_clicked(self):
        """닫기 버튼 클릭 이벤트 핸들러"""
        self.parent.close()

    def btn_min_clicked(self):
        """최소화 버튼 클릭 이벤트 핸들러"""
        self.parent.showMinimized()
