from utils import Colors, Style
from PySide6.QtWidgets import (
     QFrame, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QComboBox, QScrollArea, QCheckBox, QSlider, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QPainter, QColor
from PySide6.QtCore import Qt, QTimer, QSize, Signal
from controllers import FilterSettingController
from views.component import FilterListWidget

class BlurSettingWidget(QWidget):
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

        intensity_label = QLabel("블러 강도")
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.intensity_slider.valueChanged.connect(self.set_value_slider)  # 슬라이더 값 변경 시 이벤트 연결
        default_mosaic_layout.addWidget(intensity_label, 1, 0, 1, 2)
        default_mosaic_layout.addWidget(self.intensity_slider, 1, 3, 1, 6)


        ##########################################
        check_box_label = QLabel("배경 블러")
        self.check_background_blur = QCheckBox()
        self.check_background_blur.clicked.connect(self.set_background_blur)
        
        default_mosaic_layout.addWidget(check_box_label, 4, 0, 5, 2)
        default_mosaic_layout.addWidget(self.check_background_blur, 4, 6, 5, 7)
        
        ##########################################

        shape_label = QLabel("블러 모양")
        self.shape_combobox = QComboBox()
        self.shape_combobox.addItems(["사각형", "원형"])
        self.shape_combobox.currentIndexChanged.connect(self.set_value_drop_down)  # 드롭다운 값 변경 시 이벤트 연결
        default_mosaic_layout.addWidget(shape_label, 2, 0, 3, 2)
        default_mosaic_layout.addWidget(self.shape_combobox, 2, 4, 3, 5)
        
        default_mosaic_layout.setColumnStretch(0, 2)
        default_mosaic_layout.setColumnStretch(1, 2)
        default_mosaic_layout.setColumnStretch(2, 4)
        default_mosaic_layout.setColumnStretch(3, 4)
        default_mosaic_layout.setColumnStretch(4, 4)
        default_mosaic_layout.setColumnStretch(5, 1)
    

        default_mosaic_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
    
        layout.addLayout(default_mosaic_layout)

        self.setLayout(layout)

    def setup_mosaic_setting(self, filter_name):
        self.filter_name = filter_name
        filter_data = self.filter_controller.get_filter(filter_name)
        if filter_data:
            self.shape_combobox.setCurrentIndex(0 if filter_data.mosaic_blur_shape == "rect" else 1)
            self.intensity_slider.setValue(filter_data.mosaic_blur_strength)
            self.check_background_blur.setChecked(filter_data.background_blur)

            #self.intensity_slider2.setValue(filter_data.imgsz_mag) ##################

    def set_value_slider(self, value):
        """슬라이더 값 변경 시 호출되는 메서드"""
        self.filter_controller.update_blur_strength_in_filter(self.filter_name, value)
        self.onEventUpdate.emit()
        
    def set_background_blur(self):
        """배경 블러 활성화"""
        state = self.check_background_blur.isChecked()
        self.filter_controller.update_background_blur(self.filter_name, state)

    #########################################
    def set_value_slider2(self, value):
        """슬라이더 값 변경 시 호출되는 메서드"""
        self.filter_controller.update_imgsz_mag_in_filter(self.filter_name, value)
        self.onEventUpdate.emit()
    ########################################
    
    def set_value_drop_down(self, index):
        """드롭다운 값 변경 시 호출되는 메서드"""
        if self.filter_name:
            value = None
            if index == 0:
                value = "rect"
            elif index == 1:
                value =  "circle"
            self.filter_controller.update_blur_shape_in_filter(self.filter_name, value)
            self.onEventUpdate.emit()
            
        