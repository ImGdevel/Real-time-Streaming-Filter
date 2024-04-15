from models import Filter, FilterManager

class FilterSettingController:

    def __init__(self):
        self.filter_manager = FilterManager()
        print("호출")
        self.test = []

    def add_filter(self, filter_name: str):
        """Filter 추가 메서드"""
        if not self.get_filter(filter_name):  # 동일한 이름의 필터가 없는 경우에만 추가
            filter = Filter(name=filter_name,face_filter_on=True, face_filter=["1","2"], object_filter=["1","2"])
            self.test.append(filter)
        

    def delete_filter(self, filter_name: str):
        """Filter 삭제 메서드"""
        filter_to_delete = self.get_filter(filter_name)
        if filter_to_delete:
            self.test.remove(filter_to_delete)

        
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
        return self.test[:]
