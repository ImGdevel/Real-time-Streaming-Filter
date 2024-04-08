from views.RStreamPage import RStreamPage
from views.VideoView import VideoView
from views.ImageView import ImageView
from views.SettingsView import SettingsView
from views.HomeView import HomeView

class Router:

    def __init__(self, contentLayout, menu):
        self.contentLayout = contentLayout

        # 페이지 추가
        self.add_page(HomeView())
        self.add_page(RStreamPage())
        self.add_page(VideoView())
        self.add_page(ImageView())
        self.add_page(SettingsView())

        # Menu의 페이지 변경 시그널 연결
        menu.page_changed.connect(self.change_page)

    def add_page(self, layer):
        self.contentLayout.addWidget(layer)
        
    def change_page(self, index):
        self.contentLayout.setCurrentIndex(index)
