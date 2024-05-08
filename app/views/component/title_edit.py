from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSplitter, QCheckBox, QLineEdit
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFontMetrics
from utils import Colors, Style

class TitleEdit(QWidget):
    onEditEvent = Signal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.current_title = ""
        self.edit_mode = False

        self.initUI()
        self.setStyleSheet("font-size: 20px; padding: 0px 10px; font-weight: bold;")

    def initUI(self):
        title_layout = QHBoxLayout()
        
        self.title_label = QLabel(self.current_title)

        self.filter_name_line_edit = QLineEdit(self.current_title)
        self.filter_name_line_edit.setStyleSheet(Style.line_edit_style)
        self.filter_name_line_edit.hide()  # Hide initially

        self.title_edit_button = QPushButton("변경")
        self.title_edit_button.setMaximumWidth(70)
        self.title_edit_button.setFixedSize(60,30)
        self.title_edit_button.setStyleSheet(Style.mini_button_style)
        self.title_edit_button.clicked.connect(self.toggle_edit_mode)

        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_edit_button)
        self.filter_name_line_edit.returnPressed.connect(self.on_enter_pressed)

        self.setLayout(title_layout)
        
    def set_title(self, text : str):
        """Title Text을 수정 메서드"""
        self.title_label.setText(text)
        self.filter_name_line_edit.setText(text)
    
    def toggle_edit_mode(self,):
        """편집 모드 전환 메서드"""
        if not self.edit_mode:
            self.set_edit_mode()
        else:
            self.set_show_mode()

    def set_edit_mode(self):
        self.edit_mode = True
        self.title_edit_button.setText("저장")
        
        self.filter_name_line_edit.setText(self.title_label.text())
        filter_name_layout = self.title_label.parentWidget().layout()
        filter_name_layout.replaceWidget(self.title_label, self.filter_name_line_edit)
        self.title_label.hide()
        self.filter_name_line_edit.show()

    def set_show_mode(self):
        self.edit_mode = False
        self.title_edit_button.setText("변경")
        self.onEditEvent.emit(self.filter_name_line_edit.text())  # Emit signal
        
        # Update label text and layout
        self.title_label.setText(self.filter_name_line_edit.text())
        filter_name_layout = self.filter_name_line_edit.parentWidget().layout()
        filter_name_layout.replaceWidget(self.filter_name_line_edit, self.title_label)

        self.filter_name_line_edit.hide()
        self.title_label.show()

    def on_enter_pressed(self):
        if self.edit_mode:
            self.set_show_mode()