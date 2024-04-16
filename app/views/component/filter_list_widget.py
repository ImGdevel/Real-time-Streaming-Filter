from PyQt5.QtWidgets import QPushButton, QListWidget, QListWidgetItem
from PyQt5.QtCore import pyqtSignal
from utils import Colors

class FilterListWidget(QListWidget):
    filterButtonClicked = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.setSpacing(10)

    def add_filter(self, filter_name):
        button = QPushButton(filter_name)
        button.setStyleSheet(f'background-color: {Colors.baseColor01}; color: white;')
        button.setFixedSize(155, 40)
        item = QListWidgetItem()
        self.addItem(item)
        self.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())
        button.clicked.connect(self.emit_filter_button_clicked)

    def emit_filter_button_clicked(self):
        """필터 버튼 클릭 시그널을 발생시키는 메서드"""
        button = self.sender()
        if button:
            self.filterButtonClicked.emit(button.text())  # 시그널 발생
    
    def update_filter_list(self):

        pass