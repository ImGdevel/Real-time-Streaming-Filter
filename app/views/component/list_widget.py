from PySide6.QtWidgets import ( 
    QFrame, QWidget, QHBoxLayout,  QVBoxLayout,
    QListWidget, QListWidgetItem, QPushButton, 
    QGraphicsDropShadowEffect, QButtonGroup
)
from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor
from controllers import FilterSettingController, PersonFaceSettingController
from utils import Colors, Style

class ListWidget(QListWidget):
    onClickItemEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSpacing(15)
        self.setStyleSheet(Style.list_widget_style)

    def add_item(self, item_name):
        item = QListWidgetItem()
        self.addItem(item)
        button = self.create_button(item_name)
        self.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())

    def create_button(self, item_name):
        button = QPushButton(item_name)
        button.setObjectName("List Button")
        button.setStyleSheet(Style.list_button_style)
        button.setMinimumHeight(40)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(5)  # 흐림 정도 조절
        shadow_effect.setColor(QColor(0, 0, 0, 100))  # 그림자 색상 및 투명도 조절
        shadow_effect.setOffset(3, 3)  # 그림자 위치 조절
        button.setGraphicsEffect(shadow_effect) 

        button.clicked.connect(self.emit_button_clicked)

        return button
        

    def get_item_text(self, index: int):
        """아이템 인덱스를 통해 위젯 내의 버튼의 텍스트를 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if isinstance(widget, QPushButton):
                return widget.text()
        return None
    
    def get_item_widget(self, index: int):
        """아이템 인덱스를 통해 위젯 내의 버튼을 반환하는 메서드"""
        item = self.item(index)
        if item:
            widget = self.itemWidget(item)
            if isinstance(widget, QPushButton):
                return widget
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
        # todo : 선택된 아이템을 선택 했을때
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
            self.setCurrentRow(max(0, current_row - 1))

    def get_current_item_text(self):
        """현재 선택된 아이템의 텍스트를 반환하는 메서드"""
        current_item = self.currentItem()
        if current_item:
            widget = self.itemWidget(current_item)
            if isinstance(widget, QPushButton):
                return widget.text()
        return None

    def get_items_text(self):
        return [self.get_item_text(i) for i in range(self.count())]
    
    def set_items_event(self, event):
        self.onClickItemEvent.connect(event)


class FilterListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)
        self.filter_setting_processor = FilterSettingController()
        self.update_list()

    def create_button(self, item_name):
        button = QPushButton(item_name)
        button.setStyleSheet(Style.list_button_style)
        button.setMinimumHeight(40)
        button.setCheckable(True)
        button.clicked.connect(self.emit_button_clicked)
        self.button_group.addButton(button)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(5)  # 흐림 정도 조절
        shadow_effect.setColor(QColor(0, 0, 0, 100))  # 그림자 색상 및 투명도 조절
        shadow_effect.setOffset(3, 3)  # 그림자 위치 조절
        button.setGraphicsEffect(shadow_effect)

        return button
        
    
    def update_list(self):
        self.clear()
        lists = self.filter_setting_processor.get_filters()
        for filter in lists:
            self.add_item(filter.name)

    
class RegisteredFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.button_group = QButtonGroup()
        self.button_group.setExclusive(True)

    def add_item(self, item_name):
        item = QListWidgetItem()
        self.addItem(item)
        button = self.create_button(item_name)
        self.setItemWidget(item, button)
        item.setSizeHint(button.sizeHint())

    def create_button(self, item_name):
        """버튼을 추가하는 경우"""
        button_frame = QWidget()
        button_frame.setObjectName("Button Frame")
        button_layout = QVBoxLayout()
        button_layout.setSpacing(0)  # 레이아웃 간 간격을 0으로 설정
        button_layout.setAlignment(Qt.AlignTop)

        button = QPushButton(item_name)
        button.setObjectName("List Button")
        button.setStyleSheet(Style.list_button_style)
        button.setMinimumHeight(40)
        button.clicked.connect(self.emit_button_clicked)
        button.setCheckable(True)
        self.button_group.addButton(button)

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(5)  # 흐림 정도 조절
        shadow_effect.setColor(QColor(0, 0, 0, 100))  # 그림자 색상 및 투명도 조절
        shadow_effect.setOffset(3, 3)  # 그림자 위치 조절
        button.setGraphicsEffect(shadow_effect) 

        button_layout.addWidget(button)
        button_frame.setLayout(button_layout)

        return button_frame
    
    def button_widget_open(self):
        """버튼을 클릭하면 해당 버튼이 확장 또는 축소됨"""
        button = self.sender()
        button_frame = button.parentWidget()

        if button_frame:
            print("체크 여부", button.isChecked())

            if button.isChecked():
                # 버튼이 체크된 상태라면
                button_frame.setMinimumHeight(100)  # 프레임의 최소 높이를 확장될 높이로 설정
                print("200으로 확장!")
            else:
                # 버튼이 체크되지 않은 상태라면
                button_frame.setMinimumHeight(40)  # 프레임의 최소 높이를 원래의 최소 높이로 설정
                print("40으로 축소!")

            # 애니메이션 객체 생성
            animation = QPropertyAnimation(button_frame, b"minimumHeight")
            animation.setDuration(500)
            animation.setEasingCurve(QEasingCurve.InOutQuart)

            # 애니메이션의 시작값과 끝값 설정
            animation.setStartValue(button_frame.height())
            animation.setEndValue(button_frame.minimumHeight())

            # 애니메이션 시작
            animation.start()
            print("애니메이션 종료: ", button_frame.height())


    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        button = self.sender()

        
        
        if button:
            self.button_widget_open()
            self.onClickItemEvent.emit(button.text())  # 시그널 발생




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



class MosaicStickerList(ListWidget):
    onClickItemEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)