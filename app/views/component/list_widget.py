from PySide6.QtWidgets import ( 
    QFrame, QWidget, QHBoxLayout,  QVBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, 
    QGraphicsDropShadowEffect, QButtonGroup
)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor, QIcon
from controllers import FilterSettingController, PersonFaceSettingController
from .sticker_attach_dialog import StickerRegisteredDialog

from utils import Colors, Style

class ListWidget(QListWidget):
    onClickItemEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(15)
        self.setStyleSheet(Style.list_widget_style)
        self.current_item = None

    def add_item(self, item_name: str, item_data = None):
        item = QListWidgetItem()
        self.addItem(item)
        widget = self.create_button(item_name, item_data)
        self.setItemWidget(item, widget)
        item.setSizeHint(widget.sizeHint())

    def create_button(self, item_name: str, item_data = None):
        widget = QPushButton(item_name)
        widget.setObjectName(item_name)
        widget.setStyleSheet(Style.list_button_style)
        widget.userData = item_data
        widget.setMinimumHeight(40)
        widget.setGraphicsEffect(Style.shadow(self)) 

        widget.clicked.connect(self.emit_button_clicked)

        return widget
    
    def set_select_item(self, object_name: str):
        """해당 아이템 이름에 해당하는 오브젝트를 선택상태로 지정"""
        for i in range(self.count()):
            item = self.item(i)
            widget = self.itemWidget(item)
            if widget and widget.objectName() == object_name:
                self.setCurrentItem(item)
                self.current_item = object_name
                if isinstance(widget, QPushButton):
                    widget.setChecked(True)
                break

    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        widget = self.sender()
        
        if widget:
            self.set_select_item(widget.objectName())
            self.onClickItemEvent.emit(widget.objectName())  # ObjectName을 시그널로 전달

        
    def get_item_object_name(self, index: int):
        """아이템 인덱스를 통해 위젯 내의 오브젝트 네임을 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if widget:
                return widget.objectName()
        return None
    
    def get_item_data(self, index: int):
        """아이템 인덱스를 통해 위젯 내의 유저 데이터를 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if widget:
                return widget.userData
        return None

    def is_in_item(self, object_name: str):
        """현재 아이템 리스트에 있는지 확인"""
        for i in range(self.count()):
            if self.get_item_object_name(i) == object_name:
                return True
        return False

    def get_items_object_name(self):
        return [self.get_item_object_name(i) for i in range(self.count())]
    
    def get_items_data(self):
        return [int(self.get_item_data(i)) for i in range(self.count())]
    
    def set_items_event(self, event):
        self.onClickItemEvent.connect(event)


class FilterListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.filter_setting_processor = FilterSettingController()
        self.update_list()
    
    def create_button(self, item_name: str, item_data = None):
        widget = QPushButton(item_name)
        widget.setObjectName(item_name)
        widget.setStyleSheet(Style.list_button_style)
        widget.setMinimumHeight(40)
        widget.setCheckable(True)
        widget.clicked.connect(self.emit_button_clicked)
        self.button_group.addButton(widget)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)
        widget.setGraphicsEffect(shadow_effect) 

        return widget        
    
    def update_list(self):
        self.clear()
        lists = self.filter_setting_processor.get_filters()
        for filter in lists:
            self.add_item(filter.name)

    
class RegisteredFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_setting_processor = FilterSettingController()
        self.filter_name = None
        self.setSpacing(10)
    
    def create_button(self, item_name: str, item_data = None):
        widget = QWidget()
        widget.setObjectName(item_name)
        widget.setStyleSheet(Style.frame_style_none_line)
        widget.userData = item_data
        
        shadow_effect = QGraphicsDropShadowEffect(widget)
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)
        widget.setGraphicsEffect(shadow_effect) 
        
        frame_layout = QHBoxLayout()
        frame_layout.setContentsMargins(0,0,0,0)
        
        button = QPushButton(item_name)
        button.setObjectName(item_name)
        button.setStyleSheet(Style.list_button_style)
        button.setMinimumHeight(40)
        
        button.clicked.connect(self.emit_button_clicked)
        
        button02 = QPushButton()
        button02.setIcon(QIcon('./resources/icons/cil-smiley-sticker'))
        button02.setFixedSize(40,40)
        button02.setStyleSheet(Style.mini_button_style)
        button02.clicked.connect(self.show_sticker_dialog)
        
        button03 = QPushButton()
        button03.setFixedSize(40,40)
        button03.setStyleSheet(Style.mini_button_style)
        
        frame_layout.addWidget(button)
        frame_layout.addWidget(button02)
        frame_layout.addWidget(button03)
        widget.setLayout(frame_layout)
    
        return widget
    
    def show_sticker_dialog(self):
        self.sticker_dialog = StickerRegisteredDialog()
        self.sticker_dialog.onEventSave.connect(self.register_sticker)
    
        button = self.sender()
        if button:
            parent_widget = button.parentWidget()
            if parent_widget:
                person_id = int(parent_widget.userData)
                sticker_id = self.filter_setting_processor.get_sticker_id_in_filter(self.filter_name, person_id)
                self.sticker_dialog.set_sticker_dialog(person_id, sticker_id)
                self.sticker_dialog.exec_()
                
    
    def register_sticker(self, person_id, sticker_id):
        self.filter_setting_processor.update_sticker_id_in_filter(self.filter_name, person_id, sticker_id)
        pass
    
    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        widget = self.sender()
        
        if widget:
            self.set_select_item(widget.objectName())


    def set_filter(self, filter):
        self.filter_name = filter

    def register_person_faces(self, person_id):
        self.filter_setting_processor.add_face_in_face_filter(self.filter_name, person_id)

    def update_list(self):
        self.clear()
        for name, id in self.filter_setting_processor.get_face_in_filter(self.filter_name):
            self.add_item(name, str(id))
            
        

class AvailableFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.face_setting_processor = PersonFaceSettingController()
        self.update_list()

    def update_list(self):
        self.clear()
        for person in self.face_setting_processor.get_person_faces():
            self.add_item(person.face_name, str(person.face_id))
            

    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        widget = self.sender()
        
        if widget:
            self.set_select_item(widget.objectName())
            self.onClickItemEvent.emit(widget.userData)  # ObjectName을 시그널로 전달
    