from typing import Union
from models import Filter, AppDataSaver


class FilterManager:
    _instance = None
    filter_list: list = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def add_filter(self, filter_obj: Filter):
        """새로운 필터를 추가합니다."""
        self.filter_list.append(filter_obj)

    def update_filter(self, filtername: str, filterinfo: Filter):
        print("적용 전:", self.filter_list)
        for filter in self.filter_list:
            print("비교", filter.name, "/" , filtername, "=", filter.name == filtername)

            if filter.name == filtername:
                print("가져온 데이터", filterinfo)
                filter.name = filterinfo.name
                filter.face_filter_on = filterinfo.face_filter_on
                filter.face_filter = filterinfo.face_filter
                filter.object_filter = filterinfo.object_filter
                print("적용 후:", self.filter_list)
        

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
        return self.filter_list[:]
    
    def save_filters(self, filename: str):
        """filter_list를 파일에 저장합니다."""
        data_to_save = [filter_obj.__dict__ for filter_obj in self.filter_list]
        AppDataSaver(data_to_save).save_data(filename)

    def load_filters(self, filename: str):
        """파일에서 filter_list를 불러옵니다."""
        loaded_data = AppDataSaver(self.filter_list).load_data(filename)
        if loaded_data:
            self.filter_list = [Filter(**filter_data) for filter_data in loaded_data]
