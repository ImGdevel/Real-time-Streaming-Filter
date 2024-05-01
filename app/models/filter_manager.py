from typing import Union
from .filter_info import Filter
from .path_manager import PathManager
from .face_manager import FaceManager

class FilterManager:
    _instance = None
    filter_list: list = []
    path_manager = PathManager()
    face_manager = FaceManager()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def add_filter(self):
        filters = []
        index = 1
        for filter in self.filter_list:
            filters.append(filter.name)
        name = "New Filter "+str(index)
        while True:
            if "New Filter "+str(index) in filters:
                index += 1
                name = "New Filter "+str(index)
            else:
                self.filter_list.append(Filter(name))
                self.save_filters()
                return name

    # def add_filter(self, filter_obj: Filter):
    #     """새로운 필터를 추가합니다."""
    #     filters = []
    #     for filter in self.filter_list:
    #         filters.append(filter.name)
    #     if filter_obj.name in filters:
    #         raise ValueError("중복된 필터 이름입니다.")
    #     self.filter_list.append(filter_obj)
    #     self.save_filters()

    def update_filter(self, filtername: str, filterinfo: Filter):
        """필터를 업데이트 합니다."""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.name = filterinfo.name
                filter.face_filter_on = filterinfo.face_filter_on
                filter.face_filter = filterinfo.face_filter
                filter.object_filter = filterinfo.object_filter
                self.save_filters()
                return True
        raise ValueError("존재하지 않는 filtername입니다.")

    def update_filter_name(self, filtername: str, newname: str):
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.name = newname
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def update_filter_face_filter_on(self, filtername: str, face_filter_on: bool):
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter_on = face_filter_on
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def add_face_in_face_filter(self, filtername: str, face_id: int):
        """필터 프리셋에 얼굴 추가
        기본값으로 블러 예외 처리가 선택됨
        """
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.face_filter.keys():
                    if face == face_id:
                        self.save_filters()
                        return
                filter.face_filter[face_id] = -1
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def delete_face_in_face_filter(self, filtername: str, face_id: int):
        """필터 프리셋에서 얼굴 제거"""
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.face_filter.keys():
                    if face == face_id:
                        del filter.face_filter[face_id]
                        return
                raise ValueError("존재하지 않는 face_id입니다.")
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def init_face_in_face_filter(self, filtername:str):
        """필터 프리셋의 얼굴 필터 리스트 초기화"""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter = dict()
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def add_object_in_object_filter(self, filtername: str, object_name: str):
        """필터 프리셋에 객체 추가"""
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.object_filter:
                    if face == object_name:
                        return
                filter.object_filter.append(object_name)
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def delete_object_in_object_filter(self, filtername: str, object_name: str):
        """필터 프리셋에서 객체 제거"""
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.object_filter:
                    if face == object_name:
                        filter.object_filter.remove(object_name)
                        self.save_filters()
                        return
                raise ValueError("존재하지 않는 object_name입니다.")
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def init_object_in_object_filter(self, filtername: str):
        """오브젝트 필터 리스트를 초기화한다"""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.object_filter = []
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")
        

    def init_filter_list(self, filtername: str):
        self.init_face_in_face_filter(filtername)
        self.init_object_in_object_filter(filtername)

    def update_filter_face_filter(self, filtername: str, face_filter: dict):
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter = face_filter
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")


    def update_filter_object_filter(self, filtername: str, object_filter: list):
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.object_filter = object_filter
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")

        

    def remove_filter(self, filter_name: str):
        """지정된 이름의 필터를 제거합니다."""
        for idx, filter_obj in enumerate(self.filter_list):
            if filter_obj.name == filter_name:
                del self.filter_list[idx]
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다")

    def get_filter(self, filter_name: str) -> Union[Filter, None]:
        """이름을 기반으로 필터를 가져옵니다."""
        print("filter name: "+ filter_name)
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                return filter_obj
        return False
        #raise ValueError("존재하지 않는 filtername입니다")
    
    def get_face_names_in_filter(self, filter_name: str):
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                names = []
                for face_id in filter_obj.face_filter.keys():
                    names.append(self.face_manager.get_person_face_name(face_id))
                return names
        raise ValueError("존재하지 않는 filtername입니다.")

    def get_filters(self):
        """전체 필터 리스트를 가져옵니다."""
        return self.filter_list[:]
    
    def save_filters(self):
        """filter_list를 파일에 저장합니다."""
        self.path_manager.save_filter_data(self.filter_list)

    def load_filters(self):
        """파일에서 filter_list를 불러옵니다."""
        self.filter_list = self.path_manager.load_filter_data()
