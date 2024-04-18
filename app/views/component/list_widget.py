from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import pyqtSignal
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors

class ListWidget(QListWidget):
    onClickItemEvent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background-color: {Colors.baseColor02};')
        self.setSpacing(10)
        self.itemClicked.connect(self.emit_button_clicked)

    def add_item(self, item_name):
        button = QPushButton(item_name)
        button.setStyleSheet(f'background-color: {Colors.baseColor01}; color: white;')
        button.setFixedSize(155, 40)
        item = QListWidgetItem()
        self.addItem(item)
        self.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())
        button.clicked.connect(self.emit_button_clicked)

    def get_item_text(self, index):
        """아이템 인덱스를 통해 위젯 내의 버튼의 텍스트를 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if isinstance(widget, QPushButton):
                return widget.text()
        return None

    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        button = self.sender()
        if button:
            self.onClickItemEvent.emit(button.text())  # 시그널 발생

    def get_items_text(self):
        return [self.get_item_text(i) for i in range(self.count())]
    
    def set_items_event(self, event):
        self.onClickItemEvent.connect(event)

    
class RegisteredFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

class AvailableFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.face_setting_processor = PersonFaceSettingController()
        self.populate_faces()

    def populate_faces(self):
        for people in self.face_setting_processor.get_person_faces():
            self.add_item(people.face_name)

class FilterListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_setting_processor = FilterSettingController()
        self.filter_liat_update()
    
    def filter_liat_update(self):
        lists = self.filter_setting_processor.get_filters()
        for filter in lists:
            self.add_item(filter.name)

