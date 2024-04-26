from PySide6.QtWidgets import QListWidget, QListWidgetItem, QPushButton
from PySide6.QtCore import Signal
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors

class ListWidget(QListWidget):
    onClickItemEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
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

    def get_item_text(self, index: int):
        """아이템 인덱스를 통해 위젯 내의 버튼의 텍스트를 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if isinstance(widget, QPushButton):
                return widget.text()
        return None
    
    def is_in_item(self, index: str):
        """현재 아이템 리스트에 있는지 확인"""
        for i in range(self.count()):
            if self.get_item_text(i) == index:
                return True
        return False

    def get_item_index(self, text: str):
        """텍스트에 해당하는 항목의 인덱스를 반환하는 메서드"""
        for i in range(self.count()):
            if self.get_item_text(i) == text:
                return i
        return -1

    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        button = self.sender()
        if button:
            self.onClickItemEvent.emit(button.text())  # 시그널 발생
    
    def delete_item(self, text):
        """선택된 텍스트에 해당하는 항목 삭제"""
        for i in range(self.count()):
            if self.get_item_text(i) == text:
                self.takeItem(i)
                break

        current_row = self.currentRow()
        
        if current_row != -1:
            print("다음",current_row)
            self.setCurrentRow(max(0, current_row - 1))

    def get_current_item_text(self):
        """현재 선택된 아이템의 텍스트를 반환하는 메서드"""
        current_item = self.currentItem()
        print("현제", current_item)
        if current_item:
            widget = self.itemWidget(current_item)
            if isinstance(widget, QPushButton):
                return widget.text()
        return None

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

    def update_list(self):
        self.clear()
        print("필터 업데이트!")
        for people in self.face_setting_processor.get_person_faces():
            self.add_item(people.face_name)

class FilterListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_setting_processor = FilterSettingController()
        self.update_filter_list()
    
    def update_filter_list(self):
        self.clear()
        lists = self.filter_setting_processor.get_filters()
        for filter in lists:
            self.add_item(filter.name)
