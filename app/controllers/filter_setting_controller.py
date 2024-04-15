from models import Filter, FilterManager

class FilterSettingController:
    def __init__(self):
        self.filter_manager = FilterManager()
        self.test = []

    def add_filter(self, filter_name):
        """Filter 추가 메서드"""
        # FilterManager에 필터 추가
        self.test.append(filter_name)
        pass

    def delete_filter(self, filter_name):
        """Filter 삭제 메서드"""
        # FilterManager에서 필터 삭제
        self.test.remove(filter_name)
        pass
    
    def update_filter(self, filter: Filter = None):
        """Filter 업데이트 메서드"""
        
        pass

    def get_filters(self):

        return []
