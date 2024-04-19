from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSplitter, QCheckBox, QLineEdit
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFontMetrics
from utils import Colors

class TitleEdit(QWidget):
    onEditEvent = pyqtSignal(str)

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.current_title = ""
        self.edit_mode = False

        self.initUI()

    def initUI(self):
        title_layout = QHBoxLayout()
        
        self.tiltle_label = QLabel(self.current_title)
        self.tiltle_label.setStyleSheet('font-size: 24px;')

        self.filter_name_line_edit = QLineEdit(self.current_title)
        font_metrics = QFontMetrics(self.tiltle_label.font())
        self.filter_name_line_edit.setMinimumHeight(font_metrics.height() + 2)
        self.filter_name_line_edit.setStyleSheet('font-size: 24px;')

        self.title_edit_button = QPushButton("edit")
        self.title_edit_button.setMaximumWidth(70)
        self.title_edit_button.clicked.connect(self.toggle_edit_mode)

        title_layout.addWidget(self.tiltle_label)
        title_layout.addWidget(self.title_edit_button)

        self.filter_name_line_edit.hide()
        self.tiltle_label.show() 

        self.setLayout(title_layout)
        
    def set_title(self, text):
        self.tiltle_label.setText(text)
        
    
    def toggle_edit_mode(self):
        """편집 모드 전환 메서드"""
        if not self.edit_mode:
            self.title_edit_button.setText("save")
            self.edit_mode = True

            # QLabel을 QLineEdit로 교체
            self.filter_name_line_edit.setText(self.tiltle_label.text())
            filter_name_layout = self.tiltle_label.parentWidget().layout()
            filter_name_layout.replaceWidget(self.tiltle_label, self.filter_name_line_edit)
            self.tiltle_label.hide()
            self.filter_name_line_edit.show()
        else:
            self.title_edit_button.setText("edit")
            self.edit_mode = False
            self.onEditEvent.emit(self.filter_name_line_edit.text())
            
            # QLineEdit의 텍스트를 QLabel에 반영
            self.tiltle_label.setText(self.filter_name_line_edit.text())
            filter_name_layout = self.filter_name_line_edit.parentWidget().layout()
            filter_name_layout.replaceWidget(self.filter_name_line_edit, self.tiltle_label)

            self.filter_name_line_edit.hide()
            self.tiltle_label.show() 

