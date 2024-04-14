from models import Filter

class FilterSettingController:
    def __init__(self, filter_manager, filter_view):
        self.filter_manager = filter_manager
        self.filter_view = filter_view

        # 필요한 초기화 작업
        self.initialize()

    def initialize(self):
        """초기화 메서드"""
        # FilterManager의 데이터를 FilterSettingView에 업데이트
        self.update_filter_list_view()

        # View에서 발생하는 이벤트에 대한 연결
        self.connect_view_events()

    def update_filter_list_view(self):
        """FilterManager의 filter_list를 FilterSettingView에 업데이트"""
        # FilterManager의 filter_list를 가져와 FilterSettingView의 filter_list_widget에 업데이트
        filters = [filter_obj.name for filter_obj in self.filter_manager.filter_list]
        self.filter_view.update_filter_list(filters)

    def connect_view_events(self):
        """View에서 발생하는 이벤트에 대한 연결"""
        # FilterSettingView의 이벤트와 해당 메서드 연결
        self.filter_view.add_filter_event.connect(self.add_filter)
        self.filter_view.delete_filter_event.connect(self.delete_filter)

    def add_filter(self, filter_name):
        """Filter 추가 메서드"""
        # FilterManager에 필터 추가
        new_filter = Filter(name=filter_name)
        self.filter_manager.add_filter(new_filter)

        # FilterSettingView 업데이트
        self.update_filter_list_view()

    def delete_filter(self, filter_name):
        """Filter 삭제 메서드"""
        # FilterManager에서 필터 삭제
        self.filter_manager.remove_filter(filter_name)

        # FilterSettingView 업데이트
        self.update_filter_list_view()
