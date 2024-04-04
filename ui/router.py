from ui.SampleLayout import SampleLayout
from ui.page1 import Page1


class Router:

    def __init__(self, contentLayout, menu):
        self.contentLayout = contentLayout

        # 페이지 추가
        self.add_page(SampleLayout())
        self.add_page(Page1())

        # Menu의 페이지 변경 시그널 연결
        menu.page_changed.connect(self.change_page)

    def add_page(self, layer):
        self.contentLayout.addWidget(layer)
        
    def change_page(self, index):
        self.contentLayout.setCurrentIndex(index)
