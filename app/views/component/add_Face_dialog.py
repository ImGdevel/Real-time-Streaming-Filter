from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget,
    QLineEdit, QLabel, QFileDialog, QScrollArea, QWidget
)
from PyQt5.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PyQt5.QtCore import Qt, pyqtSignal, QSize, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon
from controllers import PersonFaceSettingController
from models import register_person
from .list_widget import AvailableFacesListWidget
from .title_edit import TitleEdit
from .file_view_widget import FileViewWidget
from .image_viewer import ImageViewWidget


class AddFaceDialog(QDialog):
    added_face = pyqtSignal(str) 
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.face_setting_processor = PersonFaceSettingController()
        self.current_person = None
        self._initUI()

    def _initUI(self):
        """다이얼로그 UI 초기화 메서드"""
        self.setWindowTitle("Add Face")
        self.setFixedSize(600, 600)

        main_layout = QHBoxLayout()

        registered_person_list_layout = self._setup_registered_person_list_layout()
        face_registration_layout = self._setup_face_registration_layout()

        main_layout.addLayout(registered_person_list_layout)
        main_layout.addLayout(face_registration_layout)

        self.setLayout(main_layout)

    def _setup_registered_person_list_layout(self):
        """registered_person_list 메서드"""
        scroll_layout = QVBoxLayout()
        self.available_faces_list_label = QLabel("FilterList")

        self.registered_person_list = AvailableFacesListWidget()
        self.registered_person_list.onClickItemEvent.connect(self.change_current_registered_person)
        self.registered_person_list.setFixedWidth(200)
        
        scroll_layout.addWidget(self.available_faces_list_label)
        scroll_layout.addWidget(self.registered_person_list)
        
        return scroll_layout

    def _setup_face_registration_layout(self):
        """얼굴 등록 레이아웃 설정 메서드"""
        face_registration_layout = QVBoxLayout()
        
        self.text_layout = TitleEdit()
        self.text_layout.onEditEvent.connect(self.change__person_name)

        image_layout = self.setup_image_layout()

        add_button = QPushButton("Register")
        add_button.clicked.connect(self.update_registered_person)
        
        face_registration_layout.addWidget(self.text_layout)
        face_registration_layout.addLayout(image_layout)
        face_registration_layout.addWidget(add_button)
        
        return face_registration_layout

    def change_current_registered_person(self, index: str):
        """등록된 사람 선택하는 메서드"""
        
        person_info = self.face_setting_processor.get_person_face(index) # 등록된 사람 가져오기 -> Face 객체
        self.current_person = person_info # 현제 선택된 사람을 person_info로 업데이트
        
        # todo : 현재 선택된 사람의 정보를 바탕으로 _setup_face_registration_layout 을 업데이트해야 함
        self.text_layout.set_title(index) #title 변경
        #        setup_image_layout에는 이미 등록된 이미지가 리스트로 들어가도록해야함

    def setup_image_layout(self):
        """이미지 업로드 레이아웃 설정 메서드"""
        image_layout = QVBoxLayout()
        
        self.image_list_widget = QListWidget()
        self.image_list_widget.setViewMode(QListWidget.IconMode)
        self.image_list_widget.setIconSize(QSize(200, 200))  # 아이콘 크기 설정
        self.image_list_widget.setResizeMode(QListWidget.Adjust)
        self.image_list_widget.setSpacing(10)  # 아이템 간 간격 설정
        
        # 드래그 앤 드롭 기능 추가
        self.image_list_widget.setDragEnabled(True)
        self.image_list_widget.setAcceptDrops(True)
        self.image_list_widget.viewport().setAcceptDrops(True)
        self.image_list_widget.setDropIndicatorShown(True)
        
        self.image_list_widget.dragEnterEvent = self.drag_enter_event
        self.image_list_widget.dragMoveEvent = self.drag_move_event
        self.image_list_widget.dropEvent = self.drop_event

        # 선택된 아이템의 배경색 및 테두리 설정
        self.image_list_widget.setStyleSheet("""
            QListWidget::item:selected {
                border: 3px solid white;
            }
        """)

        # 이미지 리스트를 업데이트
        self.update_image_list()
        
        # 스크롤 뷰 설정
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_list_widget)
        scroll_area.setFixedWidth(400)
        
        image_layout.addWidget(scroll_area)

        # 파일 탐색기 열기 버튼 추가
        upload_image_button = QPushButton("Upload Image")
        upload_image_button.clicked.connect(self.open_file_dialog)
        image_layout.addWidget(upload_image_button)
        
        return image_layout

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

        print("진행 시작")

        for idx, file_path in enumerate(image_files):
            if self.current_person.face_name:
                print("인코딩 시작")
                if register_person(self.current_person.face_name, file_path):  # 인코딩 하는 로직 인코딩이 성공하면 True / 실패하면 False
                    pixmap = QPixmap(file_path)
                    pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)
                    icon = QIcon(pixmap)

                    item = QListWidgetItem()
                    item.setIcon(icon)
                    self.image_list_widget.addItem(item)
                    self.face_setting_processor.add_person_encoding(self.current_person.face_name, file_path)
                    
                    print("인코딩 실패")
                else:
                    print(f"이미지 등록 실패: {file_path}")




    
    def update_image_list(self):
        """이미지 리스트 업데이트 메서드"""
        self.image_list_widget.clear()  # 기존 아이템 삭제
        
        if self.current_person:
            for face_id, encoding_value in self.current_person.encoding_list.items():
                pixmap = QPixmap(encoding_value)  # 이미지 경로를 QPixmap으로 변환
                pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio)  # 크기 조절 (비율 유지)
                icon = QIcon(pixmap)
                
                item = QListWidgetItem(icon, face_id)
                self.image_list_widget.addItem(item)

    def change__person_name(self, new_name):
        """이름 변경"""
        if self.current_person:
            self.face_setting_processor.update_person_name(self.current_person.face_name , new_name)
            # todo : registered_person_list를 업데이트
            
            self.text_layout.set_title(new_name) #title 변경
            self.current_person.face_name = new_name
            self.registered_person_list.update_list()


    def update_registered_person(self):
        """사람 등록"""
        if self.current_person and self.current_person.face_name:
            self.face_setting_processor.update_person_face(self.current_person.face_name, self.current_person.encoding_list)
