from models import Filter, FilterManager

class FilterSettingController:

    def __init__(self):
        self.filter_manager = FilterManager()
        print("호출")
        self.test = []

    def add_filter(self, filter_name):
        """Filter 추가 메서드"""
        filter = Filter(name=filter_name)
        self.test.append(filter)
        

    def delete_filter(self, filter_name):
        """Filter 삭제 메서드"""
        self.test.remove(filter_name)
        
    def get_filter(self, filter_name):
        """Filter를 가져오게 하기"""
        for filter in self.test:
            if filter.name == filter_name:
                return filter
        return 

    def update_filter(self, filter: Filter = None):
        """Filter 업데이트 메서드"""
        
        pass

    def get_filters(self):
        """Filter """
        return []
