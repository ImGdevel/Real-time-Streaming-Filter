from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication
from PySide6.QtGui import QPixmap, QIcon
from controllers import PersonFaceSettingController
from .list_widget import AvailableFacesListWidget
from .title_edit import TitleEdit
from utils import Style


class PersonFaceDialog(QDialog):
    updateEvent = Signal() 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.face_setting_processor = PersonFaceSettingController()
        self.current_person = None
        self.setStyleSheet(Style.frame_style)
        
        self._initUI()

    def _initUI(self):
        """다이얼로그 UI 초기화 메서드"""
        self.setWindowTitle("Add Face")
        self.setFixedSize(600, 600)

        main_layout = QHBoxLayout()
        
        
        self.face_registration_layout = self._setup_face_registration_layout()

        self.face_registration_widget = QWidget()
        self.face_registration_widget.setLayout(self.face_registration_layout)
        self.empty_widget = QWidget()

        main_layout.addWidget(self._setup_registered_person_list_layout())
        main_layout.addWidget(self.face_registration_widget)
        main_layout.addWidget(self.empty_widget)
        self.show_window(False)

        self.setLayout(main_layout)
        

    def _setup_registered_person_list_layout(self):
        """registered_person_list 메서드"""
        # Filter 목록
        list_frame = QWidget()
        list_frame.setStyleSheet(Style.list_frame_style)
        list_frame_layout = QVBoxLayout()
        
        list_label = QLabel("인물 등록")
        list_label.setStyleSheet(Style.list_frame_label)
        
        self.registered_person_list = AvailableFacesListWidget()
        self.registered_person_list.set_items_event(self.change_current_registered_person)
        self.registered_person_list.setFixedWidth(200)
       
        # Add Filter, Delete Filter 버튼
        filter_list_button_layout = QHBoxLayout()

        # Add Filter, Delete Filter 버튼
        add_button = QPushButton()
        add_button.setIcon(QIcon('./resources/icons/cil-plus.png'))
        add_button.setFixedSize(50,50)
        add_button.setStyleSheet(Style.mini_button_style)
        add_button.clicked.connect(self.add_person)
        
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('./resources/icons/Orion_bin.png'))
        delete_button.setFixedSize(50,50)
        delete_button.setStyleSheet(Style.mini_button_style)
        delete_button.clicked.connect(self.delete_person)

        filter_list_button_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        filter_list_button_layout.addWidget(add_button)
        filter_list_button_layout.addSpacing(10)  # 버튼 사이 간격
        filter_list_button_layout.addWidget(delete_button)
        
        list_frame_layout.addWidget(list_label)
        list_frame_layout.addWidget(self.registered_person_list)
        list_frame_layout.addLayout(filter_list_button_layout)
        list_frame.setLayout(list_frame_layout)
        
        return list_frame


    def _setup_face_registration_layout(self):
        """얼굴 등록 레이아웃 설정 메서드"""
        face_registration_layout = QVBoxLayout()

        self.text_layout = TitleEdit()
        self.text_layout.onEditEvent.connect(self.change_person_name)

        image_layout = self.setup_image_layout()

        #add_button = QPushButton("Register")
        #add_button.clicked.connect(self.update_registered_person)

        face_registration_layout.addWidget(self.text_layout)
        face_registration_layout.addLayout(image_layout)
        #face_registration_layout.addWidget(add_button)
        
        return face_registration_layout
    
    def show_window(self, show_window):
        """화면 """
        if show_window:
            self.empty_widget.hide()
            self.face_registration_widget.show()
        else:
            self.empty_widget.show()
            self.face_registration_widget.hide()
        

    def change_current_registered_person(self, index: str):
        """등록된 사람 선택하는 메서드"""
        self.show_window(True)
        person_info = self.face_setting_processor.get_person_face_by_id(int(index)) # 등록된 사람 가져오기 -> Face 객체

        if not person_info is None:
            self.current_person = person_info # 현제 선택된 사람을 person_info로 업데이트
            self.text_layout.set_title(self.current_person.face_name) #title 변경
            self.update_image_list()
        else:
            print("사람 정보가 존재하지 않습니다.")

    def setup_image_layout(self):
        """이미지 업로드 레이아웃 설정 메서드"""
        image_layout = QVBoxLayout()
        
        self.image_list_widget = QListWidget()
        self.image_list_widget.setViewMode(QListWidget.IconMode)
        self.image_list_widget.setFixedSize(350, 350)
        self.image_list_widget.setIconSize(QSize(200, 200))  # 아이콘 크기 설정
        self.image_list_widget.setSpacing(10)  # 아이템 간 간격 설정
        self.image_list_widget.setFlow(QListWidget.LeftToRight)
        self.image_list_widget.setWrapping(True)
        self.image_list_widget.setItemAlignment(Qt.AlignCenter)
        
        # 드래그 앤 드롭 기능 추가
        self.image_list_widget.setDragEnabled(True)
        self.image_list_widget.setAcceptDrops(True)
        self.image_list_widget.viewport().setAcceptDrops(True)
        self.image_list_widget.setDropIndicatorShown(True)
        
        self.image_list_widget.dragEnterEvent = self.drag_enter_event
        self.image_list_widget.dragMoveEvent = self.drag_move_event
        self.image_list_widget.dropEvent = self.drop_event

        image_layout.addWidget(self.image_list_widget)

        # 파일 탐색기 열기 버튼 추가
        upload_image_button = QPushButton("Upload Image")
        upload_image_button.clicked.connect(self.open_file_dialog)
        image_layout.addWidget(upload_image_button)
        
        return image_layout
    
    def add_person(self):
        """사람 추가"""
        self.face_setting_processor.add_person_face()
        self.registered_person_list.update_list()
        self.updateEvent.emit()

    def delete_person(self):
        """사람 삭제"""
        self.face_setting_processor.delete_person_face_by_id(self.current_person.face_id)
        self.registered_person_list.update_list()
        self.show_window(False)
        

    def open_file_dialog(self):
        """파일 탐색기 열기 및 이미지 추가"""
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        
        if file_paths:
            self.add_face_process(file_paths)

    def drag_enter_event(self, event):
        """드래그 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def drag_move_event(self, event):
        """드래그 이동 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def drop_event(self, event):
        """드롭 이벤트 처리"""
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            
            image_files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.add_face_process(image_files)
        else:
            event.ignore()

    def add_face_process(self, image_files):
        """이미지 등록 프로세스"""

        for idx, file_path in enumerate(image_files):
            if not self.current_person.face_name is None:
                print("인코딩 시작")
                if self.face_setting_processor.add_person_encoding_by_name(self.current_person.face_name, file_path):  # 인코딩 하는 로직 인코딩이 성공하면 True / 실패하면 False
                    pixmap = QPixmap(file_path)
                    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
                    icon = QIcon(pixmap)

                    item = QListWidgetItem()
                    item.setIcon(icon)
                    self.image_list_widget.addItem(item)
                    
                    print("인코딩 성공")
                else:
                    print(f"이미지 등록 실패: {file_path}")

    
    def update_image_list(self):
        """이미지 리스트 업데이트 메서드"""
        self.image_list_widget.clear()  # 기존 아이템 삭제

        image_list = self.face_setting_processor.get_person_encodings_by_name(self.current_person.face_name)
        if self.current_person:
            for encoding_value in image_list:
                pixmap = QPixmap(encoding_value)  # 이미지 경로를 QPixmap으로 변환
                pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)  # 크기 조절 (비율 유지)
                icon = QIcon(pixmap)
                
                item = QListWidgetItem(icon, None)
                self.image_list_widget.addItem(item)

    def change_person_name(self, new_name):
        """이름 변경"""
        if self.current_person:
            if self.face_setting_processor.update_person_name_by_name(self.current_person.face_name , new_name):
                self.text_layout.set_title(new_name) #title 변경
                self.current_person.face_name = new_name
                self.registered_person_list.update_list()
                self.updateEvent.emit()


    def update_registered_person(self):
        """사람 등록"""
        print(self.current_person)
        if self.current_person and self.current_person.face_name:
            self.face_setting_processor.update_person_face_by_name(self.current_person.face_name, self.current_person.encoding_list)
            self.updateEvent.emit()
