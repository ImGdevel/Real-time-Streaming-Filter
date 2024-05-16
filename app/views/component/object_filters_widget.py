from utils import Colors, Style
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout, QComboBox, QScrollArea, QFrame, QCheckBox
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from controllers import FilterSettingController
from views.component import FilterListWidget

class ObjectFilterSettngWidget(QWidget):
    onEventUpdate = Signal()
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        # 현재 선택된 객체 필터링 설정
        self.filter_controller = FilterSettingController()
        self.setStyleSheet(Style.frame_style)
        self.selected_filtering_object = []
        self.filter_name = None
        self.initUI()
    
    # 오브젝트 레이어
    def initUI(self):
        """객체 필터링 설정 영역 레이아웃 생성"""
        self.object_layout = QVBoxLayout()
        self.object_layout.setContentsMargins(0,0,0,0)
        self.object_layout.setAlignment(Qt.AlignTop)
        
        # QCheckBox로 변경
        self.toggle_checkbox1 = QCheckBox("담배 필터")
        self.toggle_checkbox1.userData = "cigarette"
        self.toggle_checkbox2 = QCheckBox("칼 필터")
        self.toggle_checkbox2.userData = "knife"
        self.toggle_checkbox3 = QCheckBox("로고 라벨 필터")
        self.toggle_checkbox3.userData = "logo"
        self.toggle_checkbox4 = QCheckBox("손가락 욕 필터")
        self.toggle_checkbox4.userData = "middlefinger"
        
        # 버튼에 고유한 식별자 부여
        self.toggle_checkbox1.setObjectName("cigarette")
        self.toggle_checkbox2.setObjectName("knife")
        self.toggle_checkbox3.setObjectName("logo")
        self.toggle_checkbox4.setObjectName("middlefinger")
        
        # 버튼 클릭 이벤트 연결
        self.toggle_checkbox1.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox2.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox3.clicked.connect(self.toggle_checkbox_clicked)
        self.toggle_checkbox4.clicked.connect(self.toggle_checkbox_clicked)

        # 버튼 위젯들을 QVBoxLayout에 추가
        self.object_layout.addWidget(self.toggle_checkbox1)
        self.object_layout.addWidget(self.toggle_checkbox2)
        self.object_layout.addWidget(self.toggle_checkbox3)
        self.object_layout.addWidget(self.toggle_checkbox4)
        
        self.setLayout(self.object_layout)
        
    def setup_object_filter_widget(self, filter_name):
        """객체 필터링 설정 업데이트 메서드"""
        self.filter_name = filter_name
        filter_data = self.filter_controller.get_filter(filter_name)
        filtering_object_datas = filter_data.object_filter
        
        # 기존 체크 박스들의 상태 업데이트
        for i in range(self.object_layout.count()):
            checkbox = self.object_layout.itemAt(i).widget()
            if checkbox.userData in filtering_object_datas:
                checkbox.setChecked(True)  # 체크 박스를 체크 상태로 설정
            else:
                checkbox.setChecked(False)  # 체크 박스를 체크 해제 상태로 설정
                
        self.selected_filtering_object = filtering_object_datas

        
    def toggle_checkbox_clicked(self):
        """토글 체크 박스 클릭 이벤트 핸들러"""
        sender_checkbox = self.sender()  # 이벤트를 발생시킨 체크 박스 가져오기
        checkbox_name = sender_checkbox.userData  # 체크 박스의 고유한 식별자 가져오기

        # 체크 박스 상태에 따라 리스트 업데이트
        if sender_checkbox.isChecked():
            self.selected_filtering_object.append(checkbox_name)  # 리스트에 추가
        else:
            self.selected_filtering_object.remove(checkbox_name)  # 리스트에서 제거
              
        self.filter_controller.update_filter_object_filter(self.filter_name, self.selected_filtering_object)
        self.onEventUpdate.emit()