from utils import Colors, Style
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QComboBox, QScrollArea, QFrame, QCheckBox
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from controllers import RealStreamProcessor
from views.component import FilterListWidget, ShadowWidget, FrameWidget

class ObjectFilterSettngWidget(QWidget):
    onEventUpdateCheckbox = Signal(list)
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        # 현재 선택된 객체 필터링 설정
        self.selected_filtering_object = []
        self.initUI()
    
    # 오브젝트 레이어
    def initUI(self):
        """객체 필터링 설정 영역 레이아웃 생성"""
        object_layout = QVBoxLayout()
        
        object_label = QLabel("Object Filtering")
        object_label.setStyleSheet("font-weight: bold;")
        object_label.setFixedHeight(30)  # 높이 설정
        
        self.object_setting_widget = QWidget()

        # QVBoxLayout을 self.object_setting_widget 위젯에 설정
        self.object_setting_layout = QVBoxLayout(self.object_setting_widget)
        
        # QCheckBox로 변경
        self.toggle_checkbox1 = QCheckBox("담배 필터")
        self.toggle_checkbox1.userData = "smoke"
        self.toggle_checkbox2 = QCheckBox("칼 필터")
        self.toggle_checkbox2.userData = "2"
        self.toggle_checkbox3 = QCheckBox("소주/주류 필터")
        self.toggle_checkbox3.userData = "3"
        self.toggle_checkbox4 = QCheckBox("선정성 컨텐츠 필터")
        self.toggle_checkbox4.userData = "4"
        
        # 버튼에 고유한 식별자 부여
        self.toggle_checkbox1.setObjectName("Tobacco")
        self.toggle_checkbox2.setObjectName("Knife")
        self.toggle_checkbox3.setObjectName("Bloodshed")
        self.toggle_checkbox4.setObjectName("Explicit_Content")
        
        # 버튼 클릭 이벤트 연결
        self.toggle_checkbox1.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox2.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox3.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox4.clicked.connect(self.toggle_checkbox_clicked)



        # 버튼 위젯들을 QVBoxLayout에 추가
        self.object_setting_layout.addWidget(self.toggle_checkbox1)
        self.object_setting_layout.addWidget(self.toggle_checkbox2)
        self.object_setting_layout.addWidget(self.toggle_checkbox3)
        self.object_setting_layout.addWidget(self.toggle_checkbox4)

        object_layout.addWidget(object_label)
        object_layout.addWidget(self.object_setting_widget)
        
        self.setLayout(object_layout)
        
    def setup_object_filter_widget(self, filtering_object_datas):
        """객체 필터링 설정 업데이트 메서드"""
        # 기존 체크 박스들의 상태 업데이트
        for i in range(self.object_setting_layout.count()):
            checkbox = self.object_setting_layout.itemAt(i).widget()
            if checkbox.userData in filtering_object_datas:
                checkbox.setChecked(True)  # 체크 박스를 체크 상태로 설정
            else:
                checkbox.setChecked(False)  # 체크 박스를 체크 해제 상태로 설정

        # selected_filtering_object 업데이트
        self.selected_filtering_object = filtering_object_datas.copy()
        
    def toggle_checkbox_clicked(self):
        """토글 체크 박스 클릭 이벤트 핸들러"""
        sender_checkbox = self.sender()  # 이벤트를 발생시킨 체크 박스 가져오기
        checkbox_name = sender_checkbox.userData  # 체크 박스의 고유한 식별자 가져오기

        # 체크 박스 상태에 따라 리스트 업데이트
        if sender_checkbox.isChecked():
            self.selected_filtering_object.append(checkbox_name)  # 리스트에 추가
        else:
            self.selected_filtering_object.remove(checkbox_name)  # 리스트에서 제거
        
        self.onEventUpdateCheckbox.emit(self.selected_filtering_object)