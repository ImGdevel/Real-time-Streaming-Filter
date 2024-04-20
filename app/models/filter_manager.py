from typing import Union
from models import Filter
from models.path_manager import PathManager

class FilterManager:
    _instance = None
    filter_list: list = []
    path_manager = PathManager()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add_filter(self, filter_obj: Filter):
        """새로운 필터를 추가합니다."""
        self.filter_list.append(filter_obj)

    def update_filter(self, filtername: str, filterinfo: Filter):
        """필터를 업데이트 합니다."""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.name = filterinfo.name
                filter.face_filter_on = filterinfo.face_filter_on
                filter.face_filter = filterinfo.face_filter
                filter.object_filter = filterinfo.object_filter
                print("업데이트 :", self.filter_list)
        

    def remove_filter(self, filter_name: str):
        """지정된 이름의 필터를 제거합니다."""
        for idx, filter_obj in enumerate(self.filter_list):
            if filter_obj.name == filter_name:
                del self.filter_list[idx]
                break
        else:
            print(f"Filter '{filter_name}' not found.")

    def get_filter(self, filter_name: str) -> Union[Filter, None]:
        """이름을 기반으로 필터를 가져옵니다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                return filter_obj
        return None

    def get_filters(self):
        """전체 필터 리스트를 가져옵니다."""
        return self.filter_list[:]
    
    def save_filters(self):
        """filter_list를 파일에 저장합니다."""
        self.path_manager.save_filter_data(self.filter_list)

    def load_filters(self):
        """파일에서 filter_list를 불러옵니다."""
        self.filter_list = self.path_manager.load_filter_data()
