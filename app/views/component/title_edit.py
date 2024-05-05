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
        
        self.tiltle_label = QLabel(self.current_title)

        self.filter_name_line_edit = QLineEdit(self.current_title)
        self.filter_name_line_edit.setStyleSheet(Style.line_edit_style)
        self.filter_name_line_edit.hide()  # Hide initially

        self.title_edit_button = QPushButton("edit")
        self.title_edit_button.setMaximumWidth(70)
        self.title_edit_button.clicked.connect(self.toggle_edit_mode)

        title_layout.addWidget(self.tiltle_label)
        title_layout.addWidget(self.title_edit_button)
        self.filter_name_line_edit.returnPressed.connect(self.on_enter_pressed)

        self.setLayout(title_layout)
        
    def set_title(self, text):
        self.tiltle_label.setText(text)
    
    def toggle_edit_mode(self,):
        """편집 모드 전환 메서드"""
        if not self.edit_mode:
            self.set_edit_mode()
        else:
            self.set_show_mode()

    def set_edit_mode(self):
        self.edit_mode = True
        self.title_edit_button.setText("save")

        self.filter_name_line_edit.setText(self.tiltle_label.text())
        filter_name_layout = self.tiltle_label.parentWidget().layout()
        filter_name_layout.replaceWidget(self.tiltle_label, self.filter_name_line_edit)
        self.tiltle_label.hide()
        self.filter_name_line_edit.show()

    def set_show_mode(self):
        self.edit_mode = False
        self.title_edit_button.setText("edit")
        self.onEditEvent.emit(self.filter_name_line_edit.text())  # Emit signal
        
        # Update label text and layout
        self.tiltle_label.setText(self.filter_name_line_edit.text())
        filter_name_layout = self.filter_name_line_edit.parentWidget().layout()
        filter_name_layout.replaceWidget(self.filter_name_line_edit, self.tiltle_label)

        self.filter_name_line_edit.hide()
        self.tiltle_label.show()

    def on_enter_pressed(self):
        if self.edit_mode:
            self.set_show_mode()