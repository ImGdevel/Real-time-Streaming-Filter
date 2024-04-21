from views.RealStreamView import RealStreamView
from views.VideoView import VideoView
from views.ImageView import ImageView
from views.SettingsView import SettingsView
from views.HomeView import HomeView
from views.FilterSettingView import FilterSettingView

class Router:

    def __init__(self, contentLayout, menu):
        self.contentLayout = contentLayout

        # 페이지 추가
        self.pages = [
            HomeView(),
            RealStreamView(),
            VideoView(),
            ImageView(),
            FilterSettingView(),
            SettingsView()
        ]
        
        for page in self.pages:
            self.add_page(page)

        # Menu의 페이지 변경 시그널 연결
        menu.page_changed.connect(self.change_page)

    def add_page(self, layer):
        self.contentLayout.addWidget(layer)
        
    def change_page(self, index):
        self.contentLayout.setCurrentIndex(index)
        
        # 선택된 페이지의 render 메서드 호출
        selected_page = self.pages[index]
        selected_page.render()
        
