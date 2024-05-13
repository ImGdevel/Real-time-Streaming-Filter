import sys
import os
import platform
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from modules import Ui_MainWindow
from modules import *
from widgets import *
from views import *
from utils import *
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        title = "CAMA"
        description = "CAMA APP"
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))
 
        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # EXTRA LEFT BOX
        def openCloseLeftBox():
            UIFunctions.toggleLeftBox(self, True)
        widgets.toggleLeftBox.clicked.connect(openCloseLeftBox)
        widgets.extraCloseColumnBtn.clicked.connect(openCloseLeftBox)

        # EXTRA RIGHT BOX
        def openCloseRightBox():
            UIFunctions.toggleRightBox(self, True)
        widgets.settingsTopBtn.clicked.connect(openCloseRightBox)

        # SET PAGE
        self.streaming_widget = StramingView()
        self.video_widget = VideoView()
        self.image_widget = ImageView()
        self.filter_setting_widget = FilterSettingView()
        widgets.streaming_layout.addWidget(self.streaming_widget)
        widgets.video_layout.addWidget(self.video_widget)
        widgets.image_layout.addWidget(self.image_widget)
        widgets.filter_setting_layout.addWidget(self.filter_setting_widget)

        # LEFT MENUS
        widgets.btn_home.clicked.connect(self.buttonClick)
        widgets.btn_home.setToolTip('홈')
        widgets.btn_streaming.clicked.connect(self.buttonClick)
        widgets.btn_streaming.setToolTip('실시간 스트림')
        widgets.btn_video.clicked.connect(self.buttonClick)
        widgets.btn_video.setToolTip('비디오 필터링')
        widgets.btn_image.clicked.connect(self.buttonClick)
        widgets.btn_image.setToolTip('이미지 필터링')
        widgets.btn_filter_setting.clicked.connect(self.buttonClick)
        widgets.btn_filter_setting.setToolTip('필터설정 프리셋')

        # WebCam State
        self.webcam_state = False
        self.streaming_widget.webcam_on.connect(self.webcamState)
        self.filter_setting_widget.webcam_on.connect(self.streamingStop)

        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes\\py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET HOME PAGE AND SELECT MENU
        # ///////////////////////////////////////////////////////////////
        self.current_page = widgets.home
        widgets.stackedWidget.setCurrentWidget(widgets.home)
        widgets.btn_home.setStyleSheet(UIFunctions.selectMenu(widgets.btn_home.styleSheet()))               



    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()
        
        # PRINT BTN NAME
        #print(f'Button "{btnName}" pressed!')

        # SHOW HOME PAGE
        if btnName == "btn_home" and self.current_page != widgets.home:
            widgets.stackedWidget.setCurrentWidget(widgets.home)
            self.current_page = widgets.home
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW STREAMING PAGE
        if btnName == "btn_streaming" and self.current_page != widgets.streaming_page:
            widgets.stackedWidget.setCurrentWidget(widgets.streaming_page) 
            self.current_page = widgets.streaming_page
            self.streaming_widget.render()
            UIFunctions.resetStyle(self, btnName) 
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # SHOW VIDEO PAGE
        if btnName == "btn_video" and self.current_page != widgets.video_page:
            widgets.stackedWidget.setCurrentWidget(widgets.video_page)
            self.current_page = widgets.video_page
            self.video_widget.render()
            UIFunctions.resetStyle(self, btnName)
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) 

        # SHOW IMAGE PAGE
        if btnName == "btn_image" and self.current_page != widgets.image_page:
            widgets.stackedWidget.setCurrentWidget(widgets.image_page)
            self.current_page = widgets.image_page
            self.image_widget.render()
            UIFunctions.resetStyle(self, btnName) 
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) 

        # SHOW FILTER SETTING PAGE
        if btnName == "btn_filter_setting" and self.current_page != widgets.filter_setting_page:
            widgets.stackedWidget.setCurrentWidget(widgets.filter_setting_page)
            self.current_page = widgets.filter_setting_page
            self.filter_setting_widget.render()
            UIFunctions.resetStyle(self, btnName) 
            btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet())) 

        if btnName == "btn_save":
            print("Save BTN clicked!")



    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        return
        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

    # Manage Webcam State
    def webcamState(self):
        if not self.webcam_state:
            self.webcam_state = True
    
    def streamingStop(self):
        if self.webcam_state is True:
            print("webcam stop")
            self.streaming_widget.stop_webcam()
            self.webcam_state = False

if __name__ == "__main__":
    #try:
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
    #except Exception as e:
        #print("An error occurred:", e.__class__.__name__)