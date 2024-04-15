from models import Filter, FilterManager

class FilterSettingController:
    def __init__(self, filter_manager, filter_view):
        self.filter_manager = FilterManager()

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
    
    def update_filter(self, filter: Filter = None):
        """FilterManager의 filter_list를 FilterSettingView에 업데이트"""
        pass
