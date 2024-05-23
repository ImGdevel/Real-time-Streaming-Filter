from PySide6.QtWidgets import (
    QWidget, QFrame,  QVBoxLayout, QHBoxLayout, 
    QDialog, QPushButton, QListWidget, QLabel, QFileDialog, QStackedWidget, QMessageBox
)
from PySide6.QtWidgets import QLabel, QSizePolicy, QGridLayout, QSpacerItem, QListWidgetItem, QProgressDialog
from PySide6.QtCore import Qt, Signal, QSize, QCoreApplication, QThread
from PySide6.QtGui import QPixmap, QIcon, QImage, QValidator
from controllers import PersonFaceSettingController, FaceRegistrationProcessor
from .list_widget import AvailableFacesListWidget
from .title_edit import TitleEdit
from .capture_window import CaptureWindow
from utils import Style, Icons
from models import Filtering
from models.FaceFilter import *
import cv2
import numpy as np

class PersonFaceDialog(QDialog):
    updateEvent = Signal() 
    webcam_on = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.face_setting_processor = PersonFaceSettingController()
        self.current_person = None
        self.setStyleSheet(Style.frame_style)

        self.face_detector = Filtering()
        self.capture_window = None
        
        self._initUI()

    def _initUI(self):
        """다이얼로그 UI 초기화 메서드"""
        self.setWindowTitle("Add Face")
        self.setFixedSize(600, 500)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(5,5,5,5)
        
        face_registration_list_layout = self._setup_registered_person_list_layout()
        face_registration_layout = self._setup_face_registration_layout()

        empty_widget = QWidget()
    
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(empty_widget)
        self.stacked_widget.addWidget(face_registration_layout)
        
        main_layout.addWidget(face_registration_list_layout, 1)
        main_layout.addWidget(self.stacked_widget, 3)
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
        self.registered_person_list.update_list()
       
        # Add Filter, Delete Filter 버튼
        add_button = QPushButton()
        add_button.setIcon(QIcon(Icons.plus))
        add_button.setFixedSize(50,50)
        add_button.setStyleSheet(Style.mini_button_style)
        add_button.setToolTip("인물 추가")
        add_button.setFocusPolicy(Qt.NoFocus)
        add_button.clicked.connect(self.add_person)
        
        delete_button = QPushButton()
        delete_button.setIcon(QIcon(Icons.dust_bin))
        delete_button.setFixedSize(50,50)
        delete_button.setStyleSheet(Style.mini_button_style)
        add_button.setToolTip("인물 삭제")
        delete_button.setFocusPolicy(Qt.NoFocus)
        delete_button.clicked.connect(self.delete_person)

        # Add Filter, Delete Filter 버튼
        filter_list_button_layout = QHBoxLayout()
        filter_list_button_layout.setContentsMargins(0,10,0,10)
        filter_list_button_layout.addSpacing(10)
        filter_list_button_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        filter_list_button_layout.addWidget(add_button)
        filter_list_button_layout.addWidget(delete_button)
        
        list_frame_layout.addWidget(list_label)
        list_frame_layout.addWidget(self.registered_person_list)
        list_frame_layout.addLayout(filter_list_button_layout)
        list_frame.setLayout(list_frame_layout)
        
        return list_frame


    def _setup_face_registration_layout(self):
        """얼굴 등록 레이아웃 설정 메서드"""
        frame = QFrame()
        
        self.text_layout = TitleEdit()
        self.text_layout.onEditEvent.connect(self.change_person_name)

        self.face_registration_processor = FaceRegistrationProcessor()
        self.face_registration_processor.finished.connect(self.enroll_finished)
        self.face_registration_processor.addItem.connect(self.add_image)

        self.image_list_widget = QListWidget()
        self.image_list_widget.setStyleSheet(Style.list_widget_style)
        self.image_list_widget.setViewMode(QListWidget.IconMode)
        self.image_list_widget.setFixedSize(350, 350)
        self.image_list_widget.setIconSize(QSize(200, 200))  # 아이콘 크기 설정
        self.image_list_widget.setSpacing(10)  # 아이템 간 간격 설정
        self.image_list_widget.setFlow(QListWidget.LeftToRight)
        self.image_list_widget.setWrapping(True)
        self.image_list_widget.setItemAlignment(Qt.AlignCenter)
        self.image_list_widget.setDragEnabled(True)
        self.image_list_widget.setAcceptDrops(True)
        self.image_list_widget.viewport().setAcceptDrops(True)
        self.image_list_widget.setDropIndicatorShown(True)
        self.image_list_widget.setFocusPolicy(Qt.NoFocus)
        
        self.image_list_widget.dragEnterEvent = self.drag_enter_event
        self.image_list_widget.dragMoveEvent = self.drag_move_event
        self.image_list_widget.dropEvent = self.drop_event
        
        image_list_label = QLabel("등록된 얼굴")
        image_list_label.setStyleSheet(Style.title_label)
        image_list_label.setFixedHeight(45)
        
        # 파일 탐색기 열기 버튼 추가
        upload_image_button = QPushButton()
        upload_image_button.setIcon(QIcon(Icons.folder_open))
        upload_image_button.setStyleSheet(Style.mini_button_style)
        upload_image_button.setFixedSize(45, 45)
        upload_image_button.setToolTip("파일 탐색")
        upload_image_button.setFocusPolicy(Qt.NoFocus)
        upload_image_button.clicked.connect(self.open_file_dialog)
        
        capture_button = QPushButton()
        capture_button.setIcon(QIcon(Icons.camera))
        capture_button.setStyleSheet(Style.mini_button_style)
        capture_button.setFixedSize(45, 45)
        capture_button.setToolTip("얼굴 화면 캡쳐")
        capture_button.setFocusPolicy(Qt.NoFocus)
        capture_button.clicked.connect(self.open_capture_window)
        
        image_layout = QGridLayout()
        image_layout.addWidget(self.text_layout, 0, 0, 1 ,7, Qt.AlignVCenter)
        image_layout.addWidget(image_list_label, 1, 0, 2, 4, Qt.AlignTop)
        image_layout.addWidget(capture_button, 1, 5, Qt.AlignRight)
        image_layout.addWidget(upload_image_button, 1, 6, Qt.AlignRight)
        image_layout.addWidget(self.image_list_widget, 2, 0, 3, 7)
        frame.setLayout(image_layout)
        
        return frame
    
    def add_face_process(self, images: list[QPixmap]):
        """이미지 등록 프로세스"""
        try:
            self.progress_dialog = QProgressDialog()
            self.progress_dialog.setWindowTitle("Progress")
            self.progress_dialog.setLabelText("얼굴을 등록 중 입니다")
            self.progress_dialog.setCancelButtonText("취소")
            self.progress_dialog.setRange(0, 0)
            self.progress_dialog.canceled.connect(self.cancel_progress)
            
            self.face_registration_processor.setup(images, self.current_person)
            self.face_registration_processor.start()
            
            self.progress_dialog.exec()
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("얼굴 등록에 실패 했습니다")
            msg.setWindowTitle("경고")
            msg.exec_()
            
        
    def enroll_finished(self, result : int):
        """이미지 등록 완료"""
        self.progress_dialog.close()
        self.sucess = result
        if result == 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("얼굴 등록에 실패했습니다 \n\n다음 사진은 등록할 수 없습니다\n1) 얼굴을 인식하기 어려운 사진 \n2) 두 명 이상 얼굴이 촬영된 사진")
            msg.setWindowTitle("경고")
            msg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("얼굴이 등록되었습니다")
            msg.setWindowTitle("알림")
            msg.exec_()
            

    def cancel_progress(self):
        """등록 취소"""
        self.face_registration_processor.cancel()
        self.face_registration_processor.quit()
        self.face_registration_processor.wait()
    
    def open_capture_window(self):
        """사진 캡쳐 페이지 Open"""
        try:
            self.webcam_on.emit()
            self.capture_window = CaptureWindow()
            self.capture_window.photo_captured.connect(self.receive_photo_from_capture)
            self.capture_window.exec_()
        except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("얼굴 촬영에 실패했습니다.")
            msg.setWindowTitle("경고")
            msg.exec_()
            self.capture_window.close()
        
    def receive_photo_from_capture(self, photo):
        """이미지 등록이 완료된 이미지를 받습니다"""
        self.add_face_process([photo])
        self.update_image_list()
    
    def show_window(self, show_window):
        """화면 """
        if not show_window:
            self.stacked_widget.setCurrentIndex(0)
        else:
            self.stacked_widget.setCurrentIndex(1)

    def change_current_registered_person(self, current_person_index):
        """등록된 사람 선택하는 메서드"""
        self.show_window(True)
        self.registered_person_list.update_list()
        person_info = self.face_setting_processor.get_person_face_by_id(int(current_person_index)) # 등록된 사람 가져오기 -> Face 객체
        if not person_info is None:
            self.current_person = person_info # 현제 선택된 사람을 person_info로 업데이트
            self.text_layout.set_title(self.current_person.face_name) #title 변경
            self.update_image_list()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("존재하지 않는 사람입니다")
            msg.setWindowTitle("알림")
            msg.exec_()
            self.update_image_list()
    
    def add_person(self):
        """사람 추가"""
        self.face_setting_processor.add_person_face()
        self.registered_person_list.update_list()
        self.updateEvent.emit()

    def delete_person(self):
        """사람 삭제"""
        if self.face_setting_processor.get_person_face_by_id(self.current_person.face_id) is not None:
            self.face_setting_processor.delete_person_face_by_id(self.current_person.face_id)
        self.registered_person_list.update_list()
        self.updateEvent.emit()
        self.show_window(False)

    def open_file_dialog(self):
        """파일 탐색기 열기 및 이미지 추가"""
        options = QFileDialog.Options()
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Open Images", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        
        if file_paths:
            images = []
            #file_paths 를 QPizmap으로 변환
            for path in file_paths:
                image = cv2.imread(path)
                images.append(image)
            self.add_face_process(images)

    def update_image_list(self):
        """이미지 리스트 업데이트 메서드"""
        self.image_list_widget.clear()  # 기존 아이템 삭제
        image_list = self.face_setting_processor.get_person_encodings_by_name(self.current_person.face_name)
        if image_list is None:
            QMessageBox.warning(None, "경고", "존재하지 않는 이름입니다.", QMessageBox.Ok)
            self.delete_person()
            return
        if self.current_person:
            for encoding_value in image_list:
                self.add_image(encoding_value)
                
    def add_image(self, img: QImage):
        """이미지 리스트에 이미지 등록"""
        pixmap = QPixmap(img)
        pixmap = pixmap.scaled(140, 140, Qt.KeepAspectRatio)  # 크기 조절 (비율 유지)
        icon = QIcon(pixmap)
        item = QListWidgetItem(icon, None)
        self.image_list_widget.addItem(item)

    def change_person_name(self, new_name):
        """이름 변경"""
        validator = self.text_layout.filter_name_line_edit.validator()
        state, _, _ = validator.validate(new_name,0)
        print("update face name:", state)

        if state == QValidator.Acceptable:
            if self.current_person:
                if self.current_person.face_name == new_name:
                    return
                if self.face_setting_processor.update_person_name_by_name(self.current_person.face_name , new_name):
                    self.change_current_registered_person(self.current_person.face_id)
                    self.updateEvent.emit()
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
                    msg.setText("이미 등록된 사람이 있습니다")
                    msg.setWindowTitle("경고")
                    msg.exec_()
                    self.change_current_registered_person(self.current_person.face_id)
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowFlags(msg.windowFlags() | Qt.WindowStaysOnTopHint)
            msg.setText("유효하지 않은 이름입니다")
            msg.setWindowTitle("경고")
            msg.exec_()
            self.change_current_registered_person(self.current_person.face_id)

            

    # def update_registered_person(self):
    #     """사람 등록"""
    #     print(self.current_person)
    #     if self.current_person and self.current_person.face_name:
    #         self.face_setting_processor.update_person_face_by_name(self.current_person.face_name, self.current_person.encoding_list)
    #         self.updateEvent.emit()
    
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
            images = []
            #file_paths 를 QPizmap으로 변환
            for path in image_files:
                image = cv2.imread(path)
                images.append(image)
            self.add_face_process(images)
        else:
            event.ignore()
    
        # Close Event
    def closeEvent(self, event):
        if self.capture_window is not None:
            self.capture_window.close()