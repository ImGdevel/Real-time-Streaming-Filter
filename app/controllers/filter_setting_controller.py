from models import FilterManager, Filter, FaceManager

class FilterSettingController:

    def __init__(self):
        self.filter_manager = FilterManager()
        self.face_manager = FaceManager()
        self.load_filter()

    def add_filter(self):
        """새로운 필터 프리셋을 생성한다."""
        return self.filter_manager.add_filter()

    def add_face_in_filter(self, filter_name: str, person_id: int):
        """필터 프리셋에 얼굴 추가
        기본값으로 블러 예외 처리가 선택됨
        """
        self.filter_manager.add_face_in_filter(filter_name, person_id)

    def add_object_in_filter(self, filter_name: str, object_name: str):
        """필터 프리셋에 객체 추가"""
        self.filter_manager.add_object_in_filter(filter_name, object_name)
        
    def get_filter(self, filter_name):
        """Filter를 가져오게 하기"""
        return self.filter_manager.get_filter(filter_name)

    def get_face_names_in_filter(self, filter_name: str):
        """필터에서 face_name리스트를 반환한다"""
        ids = self.filter_manager.get_face_ids_in_filter(filter_name)
        names = []
        for id in ids:
            names.append(self.face_manager.get_person_face_name(id))
        return names
    
    def get_face_ids_in_filter(self, filter_name: str):
        """필터에서 face_id리스트를 반환한다."""
        return self.filter_manager.get_face_ids_in_filter(filter_name)
        
    def get_face_in_filter(self, filter_name: str):
        """필터에서 (face_id, sticker_id) 리스트를 반환한다"""
        ids = self.filter_manager.get_face_ids_in_filter(filter_name)
        names = []
        
        for id in ids:
            name = self.face_manager.get_person_face_name(id)
            names.append((name, id))
            
        return names
    
    def get_sticker_id_in_filter(self, filter_name: str, face_id: int):
        """필터 프리셋의 face_id에 부여된 sticker_id를 반환한다."""
        return self.filter_manager.get_sticker_id_in_filter(filter_name, face_id)

    def get_blur_strength_in_filter(self, filter_name: str):
        """필터 프리셋의 blur 강도를 반환한다."""
        return self.filter_manager.get_blur_strength_in_filter(filter_name)

    def get_blur_shape_in_filter(self, filter_name: str):
        """필터 프리셋의 blur 모양을 반환한다."""
        return self.filter_manager.get_blur_shape_in_filter(filter_name)
    
    def get_imgsz_mag_in_filter(self, filter_name: str):
        """필터 프리셋의 imgsz_mag를 반환한다."""
        return self.filter_manager.get_imgsz_mag_in_filter(filter_name)

    def get_filters(self):
        """Filter """
        return self.filter_manager.get_filters()   
    
    def update_filter(self, filter_target_name: str, filter_name: str, face_filter_on: bool, updated_face_filter: list, updated_object_filter: list):
        """Filter 업데이트 메서드"""
        if self.filter_manager.get_filter(filter_target_name):
            update_filter = Filter(filter_name, face_filter_on, updated_face_filter, updated_object_filter)
            self.filter_manager.update_filter(filter_target_name, update_filter)
            print(f"Filter '{filter_name}'의 face_filter 정보가 업데이트 되었습니다.")
        else:
            print(f"Filter '{filter_name}'를 찾을 수 없습니다.")
            
    def update_filter_name(self, filter_target_name: str, filter_new_name: str):
        """필터 프리셋의 이름을 변경한다"""
        return self.filter_manager.update_filter_name(filter_target_name, filter_new_name)

    def update_filter_face_filter_on(self, filter_name: str, face_filter_on: bool):
        """필터 프리셋의 얼굴 필터링 여부를 변경한다"""
        return self.filter_manager.update_filter_face_filter_on(filter_name, face_filter_on)
    
    def update_filter_face_filter(self, filter_name: str, face_filter: dict):
        """필터 프리셋의 얼굴 리스트를 변경한다."""
        self.filter_manager.update_filter_face_filter(filter_name, face_filter)

    def update_filter_object_filter(self, filter_name: str, object_filter: list):
        """필터 프리셋의 객체 리스트를 변경한다."""
        self.filter_manager.update_filter_object_filter(filter_name, object_filter)

    def update_sticker_id_in_filter(self, filter_name: str, face_id: int, sticker_id: int):
        """필터 프리셋의 face_id에 부여된 sticer_id를 변경한다."""
        self.filter_manager.update_sticker_id_in_filter(filter_name, face_id, sticker_id)

    def update_blur_strength_in_filter(self, filter_name: str, blur_strength: float):
        """필터 프리셋의 blur 강도를 변경한다."""
        return self.filter_manager.update_blur_strength_in_filter(filter_name, blur_strength)

    def update_blur_shape_in_filter(self, filter_name: str, blur_shape: str):
        """필터 프리셋의 blur 모양을 변경한다."""
        return self.filter_manager.update_blur_shape_in_filter(filter_name, blur_shape)
    
    def update_imgsz_mag_in_filter(self, filter_name: str, imgsz_mag: float):
        """필터 프리셋의 imgsz_mag를 변경한다."""
        return self.filter_manager.update_imgsz_mag_in_filter(filter_name, imgsz_mag)

    def delete_filter(self, filter_name: str):
        """Filter 삭제 메서드"""
        if self.filter_manager.get_filter(filter_name):
            self.filter_manager.remove_filter(filter_name)

    def delete_face_in_filter(self, filter_name: str, face_id: int):
        """필터 프리셋에서 얼굴 제거"""
        return self.filter_manager.delete_face_in_filter(filter_name, face_id)
    
    def delete_object_in_filter(self, filter_name: str, object_name: str):
        """필터 프리셋에서 객체 제거"""
        return self.filter_manager.delete_object_in_filter(filter_name, object_name)
    
    def init_face_in_filter(self, filter_name: str):
        """필터 프리셋의 얼굴 필터 리스트 초기화"""
        return self.filter_manager.init_face_in_filter(filter_name)
    
    def init_object_in_filter(self, filter_name: str):
        """오브젝트 필터 리스트를 초기화한다"""
        return self.filter_manager.init_object_in_filter(filter_name)

    def init_filter(self, filter_name: str):
        """필터 내용 초기화"""
        return self.filter_manager.init_filter(filter_name)

    def save_filter(self):
        """필터를 로컬에 저장합니다"""
        self.filter_manager.save_filters()

    def load_filter(self):
        """필터를 로컬에서 가져옵니다."""
        self.filter_manager.load_filters()
