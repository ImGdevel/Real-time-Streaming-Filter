from utils import Colors, Style
from PySide6.QtWidgets import (
     QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QScrollArea, QCheckBox, QSlider, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from controllers import FilterSettingController
from views.component import FilterListWidget

class DetectSettingWidget(QWidget):
    onEventUpdate = Signal()
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.filter_controller = FilterSettingController()
        self.filter_name = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        default_mosaic_layout = QGridLayout()
        default_mosaic_layout.setSpacing(10)

        ##########################################
        intensity_label2 = QLabel("감지 심도")
        self.intensity_slider2 = QSlider(Qt.Horizontal)
        self.intensity_slider2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.intensity_slider2.valueChanged.connect(self.set_value_slider2)  # 슬라이더 값 변경 시 이벤트 연결

        default_mosaic_layout.addWidget(intensity_label2, 3, 0, 4, 2)
        default_mosaic_layout.addWidget(self.intensity_slider2, 3, 3, 4, 6)
        ##########################################
        ##########################################
        intensity_label3 = QLabel("감지 정확도")
        self.intensity_slider3 = QSlider(Qt.Horizontal)
        self.intensity_slider3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.intensity_slider3.valueChanged.connect(self.set_value_slider3)  # 슬라이더 값 변경 시 이벤트 연결

        default_mosaic_layout.addWidget(intensity_label3, 1, 0, 2, 2)
        default_mosaic_layout.addWidget(self.intensity_slider3, 1, 3, 2, 6)
        ##########################################
        
        default_mosaic_layout.setColumnStretch(0, 2)
        default_mosaic_layout.setColumnStretch(1, 2)
        default_mosaic_layout.setColumnStretch(2, 4)
        default_mosaic_layout.setColumnStretch(3, 4)
        default_mosaic_layout.setColumnStretch(4, 4)
        default_mosaic_layout.setColumnStretch(5, 1)
    

        default_mosaic_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
    
        layout.addLayout(default_mosaic_layout)

        self.setLayout(layout)

    def setup_detect_setting(self, filter_name):
        self.filter_name = filter_name
        filter_data = self.filter_controller.get_filter(filter_name)
        if filter_data:
            self.intensity_slider2.setValue(filter_data.imgsz_mag) ##################
            self.intensity_slider3.setValue(filter_data.predict_conf) ##################
    

    #########################################
    def set_value_slider2(self, value):
        """슬라이더 값 변경 시 호출되는 메서드"""
        self.filter_controller.update_imgsz_mag_in_filter(self.filter_name, value)
        self.onEventUpdate.emit()
    ########################################
    #########################################
    def set_value_slider3(self, value):
        """슬라이더 값 변경 시 호출되는 메서드"""
        self.filter_controller.update_predict_conf_in_filter(self.filter_name, value)
        self.onEventUpdate.emit()
    ########################################

        