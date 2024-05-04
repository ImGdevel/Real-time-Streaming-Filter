from utils import Colors, Style
from PySide6.QtWidgets import (
     QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QScrollArea, QCheckBox, QSlider, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from controllers import FilterSettingController
from views.component import FilterListWidget, ShadowWidget, FrameWidget

class MosaicSettingWidget(QWidget):
    onEventUpdateCheckbox = Signal(list)
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.filter_controller = FilterSettingController()
        
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        default_mosaic_layout = QGridLayout()
        default_mosaic_layout.setSpacing(10)

        default_mosaic_layout_label = QLabel("기본 모자이크 설정")
        default_mosaic_layout_label.setStyleSheet(Style.title_label)
        default_mosaic_layout.addWidget(default_mosaic_layout_label, 0, 0)

        intensity_label = QLabel("모자이크 강도 ")
        intensity_slider = QSlider(Qt.Horizontal)
        intensity_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        intensity_slider.valueChanged.connect(self.set_value_slider)  # 슬라이더 값 변경 시 이벤트 연결
        
        slider_value_label = QLabel("0")
        
        default_mosaic_layout.addWidget(intensity_label, 1, 0)
        default_mosaic_layout.addWidget(slider_value_label, 1, 1, alignment=Qt.AlignRight)
        default_mosaic_layout.addWidget(intensity_slider, 1, 2, alignment=Qt.AlignRight)
        

        shape_label = QLabel("모자이크 모양 ")
        shape_combobox = QComboBox()
        shape_combobox.addItems(["사각형", "원형"])
        shape_combobox.currentIndexChanged.connect(self.set_value_drop_down)  # 드롭다운 값 변경 시 이벤트 연결
        default_mosaic_layout.addWidget(shape_label, 2, 0)
        default_mosaic_layout.addWidget(shape_combobox, 2, 1, 2, 2, alignment=Qt.AlignRight)
        
        default_mosaic_layout.setColumnStretch(0, 1)
        default_mosaic_layout.setColumnStretch(1, 1)
        default_mosaic_layout.setColumnStretch(2, 8)

        default_mosaic_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
    
        layout.addLayout(default_mosaic_layout)

        self.setLayout(layout)
    
    def set_value_slider(self, value):
        """슬라이더 값 변경 시 호출되는 메서드"""
        print("Slider value changed:", value)
    
    
    def set_value_drop_down(self, index):
        """드롭다운 값 변경 시 호출되는 메서드"""
        value = None
        if index == 0:
            value = "rect"
        elif index == 1:
            value =  "circle"
            
        