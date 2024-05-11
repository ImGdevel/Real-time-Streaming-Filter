from typing import Union
from .filter_info import Filter
from .path_manager import PathManager
# from .face_manager import FaceManager

class FilterManager:
    _instance = None
    filter_list: list[Filter] = []
    path_manager = PathManager()
    # face_manager = FaceManager()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def add_filter(self):
        """새로운 필터 프리셋을 생성한다."""
        filters = []
        index = 1
        for filter in self.filter_list:
            filters.append(filter.name)
        name = "새 필터 "+str(index)
        while True:
            if "새 필터 "+str(index) in filters:
                index += 1
                name = "새 필터 "+str(index)
            else:
                self.filter_list.append(Filter(name))
                self.save_filters()
                return name

    def add_face_in_filter(self, filtername: str, face_id: int):
        """필터 프리셋에 얼굴 추가
        기본값으로 블러 예외 처리가 선택됨
        """
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.face_filter.keys():
                    if int(face) == face_id:
                        self.save_filters()
                        return
                filter.face_filter[int(face_id)] = -1
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def add_object_in_filter(self, filtername: str, object_name: str):
        """필터 프리셋에 객체 추가"""
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.object_filter:
                    if face == object_name:
                        return
                filter.object_filter.append(object_name)
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def get_filter(self, filter_name: str) -> Union[Filter, None]:
        """이름을 기반으로 필터를 가져옵니다."""
        if filter_name is None:
            return False
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                return filter_obj
        return False
        #raise ValueError("존재하지 않는 filtername입니다")
    
    def get_face_ids_in_filter(self, filter_name: str):
        """필터 프리셋의 face_id 리스트를 반환한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                ids = []
                for face_id in filter_obj.face_filter.keys():
                    ids.append(int(face_id))
                return ids
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def get_sticker_id_in_filter(self, filter_name: str, face_id: int):
        """필터 프리셋의 face_id에 부여된 sticker_id를 반환한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                for key in filter_obj.face_filter.keys():
                    if int(key) == face_id:
                        return filter_obj.face_filter[key]
                raise ValueError("존재하지 않는 face_id입니다")
        raise ValueError("존재하지 않는 filtername입니다.")

    def get_blur_strength_in_filter(self, filter_name: str):
        """필터 프리셋의 blur 강도를 반환한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                return filter_obj.blur_strength
        raise ValueError("존재하지 않는 filtername입니다.")    

    def get_blur_shape_in_filter(self, filter_name: str):
        """필터 프리셋의 blur 모양을 반환한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                return filter_obj.blur_shape
        raise ValueError("존재하지 않는 filtername입니다.")   
     
    def get_filters(self):
        """전체 필터 리스트를 가져옵니다."""
        return self.filter_list[:]

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
        """필터 프리셋의 이름을 변경한다"""
        for filter in self.filter_list:
            if filter.name == newname:
                return False
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.name = newname
                self.save_filters()
                return True
        return False

    def update_filter_face_filter_on(self, filtername: str, face_filter_on: bool):
        """필터 프리셋의 얼굴 필터링 여부를 변경한다"""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter_on = face_filter_on
                self.save_filters()
                return True
        return False

    def update_filter_face_filter(self, filtername: str, face_filter: dict):
        """필터 프리셋의 얼굴 리스트를 변경한다."""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter = face_filter
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")


    def update_filter_object_filter(self, filtername: str, object_filter: list):
        """필터 프리셋의 객체 리스트를 변경한다."""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.object_filter = object_filter
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")

    def update_sticker_id_in_filter(self, filter_name: str, face_id: int, sticker_id: int):
        """필터 프리셋의 face_id에 부여된 sticer_id를 변경한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                for key in filter_obj.face_filter.keys():
                    if int(key) == face_id:
                        filter_obj.face_filter[key] = sticker_id
                        self.save_filters()
                        return filter_obj.face_filter[key]
                raise ValueError("존재하지 않는 face_id입니다")
        raise ValueError("존재하지 않는 filtername입니다.")    
    
    def update_blur_strength_in_filter(self, filter_name: str, blur_strength: float):
        """필터 프리셋의 blur 강도를 변경한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                filter_obj.mosaic_blur_strength = blur_strength
                #print("blur strength:",blur_strength)
                return
        print("filterName:", filter_name)
        raise ValueError("존재하지 않는 filtername입니다.")    

    def update_blur_shape_in_filter(self, filter_name: str, blur_shape: str):
        """필터 프리셋의 blur 모양을 변경한다."""
        for filter_obj in self.filter_list:
            if filter_obj.name == filter_name:
                filter_obj.mosaic_blur_shape = blur_shape
                #print("blur shape:",blur_shape)
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

    def delete_face_in_filter(self, filtername: str, face_id: int):
        """필터 프리셋에서 얼굴 제거"""
        for filter in self.filter_list:
            if filter.name == filtername:
                for face in filter.face_filter.keys():
                    if int(face) == face_id:
                        del filter.face_filter[face_id]
                        return
                return
        raise ValueError("존재하지 않는 filtername입니다.")
    
    def delete_object_in_filter(self, filtername: str, object_name: str):
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
    
    def init_face_in_filter(self, filtername:str):
        """필터 프리셋의 얼굴 필터 리스트 초기화"""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.face_filter = dict()
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")


    
    def init_object_in_filter(self, filtername: str):
        """오브젝트 필터 리스트를 초기화한다"""
        for filter in self.filter_list:
            if filter.name == filtername:
                filter.object_filter = []
                self.save_filters()
                return
        raise ValueError("존재하지 않는 filtername입니다.")
        

    def init_filter(self, filtername: str):
        """필터 내용 초기화"""
        self.init_face_in_filter(filtername)
        self.init_object_in_filter(filtername)
 


    def save_filters(self):
        """filter_list를 파일에 저장합니다."""
        self.path_manager.save_filter_data(self.filter_list)

    def load_filters(self):
        """파일에서 filter_list를 불러옵니다."""
        self.filter_list = self.path_manager.load_filter_data()
