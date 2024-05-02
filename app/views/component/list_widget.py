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

        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(5)
        shadow_effect.setColor(QColor(0, 0, 0, 100))
        shadow_effect.setOffset(3, 3)
        widget.setGraphicsEffect(shadow_effect) 

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

    def is_in_item(self, object_name: str):
        """현재 아이템 리스트에 있는지 확인"""
        for i in range(self.count()):
            if self.get_item_object_name(i) == object_name:
                return True
        return False

    def get_items_object_name(self):
        return [self.get_item_object_name(i) for i in range(self.count())]
    
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


    def set_filter(self, filter):
        self.filter_name = filter

    def register_person_faces(self, person_id):
        print("받음", person_id, "전송 >", self.filter_name, person_id)
        
        self.filter_setting_processor.add_face_in_face_filter(self.filter_name, person_id)

    def update_list(self):
        self.clear()
        lists = self.filter_setting_processor.get_face_names_in_filter(self.filter_name)
        for filter in self.filter_setting_processor.get_face_names_in_filter(self.filter_name):
            print("필터 사람", filter)
            self.add_item(filter)


    # def add_item(self, item_name):
    #     item = QListWidgetItem()
    #     self.addItem(item)
    #     button = self.create_button(item_name)
    #     self.setItemWidget(item, button)
    #     item.setSizeHint(button.sizeHint())

    # def create_button(self, item_name):
    #     """버튼을 추가하는 경우"""
    #     button_frame = QWidget()
    #     button_frame.setObjectName("Button Frame")
    #     button_layout = QVBoxLayout()
    #     button_layout.setSpacing(0)  # 레이아웃 간 간격을 0으로 설정
    #     button_layout.setAlignment(Qt.AlignTop)

    #     button = QPushButton(item_name)
    #     button.setObjectName("List Button")
    #     button.setStyleSheet(Style.list_button_style)
    #     button.setMinimumHeight(40)
    #     button.clicked.connect(self.emit_button_clicked)
    #     button.setCheckable(True)
    #     self.button_group.addButton(button)

    #     shadow_effect = QGraphicsDropShadowEffect(self)
    #     shadow_effect.setBlurRadius(5)  # 흐림 정도 조절
    #     shadow_effect.setColor(QColor(0, 0, 0, 100))  # 그림자 색상 및 투명도 조절
    #     shadow_effect.setOffset(3, 3)  # 그림자 위치 조절
    #     button.setGraphicsEffect(shadow_effect) 

    #     #button_layout.addWidget(button)
    #     #button_frame.setLayout(button_layout)

    #     return button
    
    # def button_widget_open(self):
    #     """버튼을 클릭하면 해당 버튼이 확장 또는 축소됨"""
    #     button = self.sender()
    #     button_frame = button.parentWidget()

    #     if button_frame:
    #         print("체크 여부", button.isChecked())

    #         if button.isChecked():
    #             # 버튼이 체크된 상태라면
    #             button_frame.setMinimumHeight(100)  # 프레임의 최소 높이를 확장될 높이로 설정
    #             print("200으로 확장!")
    #         else:
    #             # 버튼이 체크되지 않은 상태라면
    #             button_frame.setMinimumHeight(40)  # 프레임의 최소 높이를 원래의 최소 높이로 설정
    #             print("40으로 축소!")

    #         # 애니메이션 객체 생성
    #         animation = QPropertyAnimation(button_frame, b"minimumHeight")
    #         animation.setDuration(500)
    #         animation.setEasingCurve(QEasingCurve.InOutQuart)

    #         # 애니메이션의 시작값과 끝값 설정
    #         animation.setStartValue(button_frame.height())
    #         animation.setEndValue(button_frame.minimumHeight())

    #         # 애니메이션 시작
    #         animation.start()
    #         print("애니메이션 종료: ", button_frame.height())


    # def emit_button_clicked(self):
    #     """아이템 클릭 시그널을 발생시키는 메서드"""
    #     button = self.sender()

        
        
    #     if button:
    #         self.button_widget_open()
    #         self.onClickItemEvent.emit(button.text())  # 시그널 발생



class AvailableFacesListWidget(ListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.face_setting_processor = PersonFaceSettingController()
        self.update_list()

    def update_list(self):
        self.clear()
        print("필터 업데이트!")
        for person in self.face_setting_processor.get_person_faces():
            print("사람:", person)

            self.add_item(person.face_name, str(person.face_id))

    def emit_button_clicked(self):
        """아이템 클릭 시그널을 발생시키는 메서드"""
        widget = self.sender()
        
        if widget:
            self.set_select_item(widget.objectName())
            print("전송>>" ,widget.userData, type(widget.userData))
            self.onClickItemEvent.emit(widget.userData)  # ObjectName을 시그널로 전달
    



class MosaicStickerList(ListWidget):
    onClickItemEvent = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)