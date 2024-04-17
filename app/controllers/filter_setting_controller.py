from models import Filter, FilterManager

class FilterSettingController:

    def __init__(self):
        self.filter_manager = FilterManager()
        self.test = []

    def add_filter(self, filter_name: str):
        """Filter 추가 메서드"""
        if not self.get_filter(filter_name):  # 동일한 이름의 필터가 없는 경우에만 추가
            filter = Filter(name=filter_name,face_filter_on=True, face_filter=[], object_filter=[])
            self.filter_manager.add_filter(filter)
            self.test.append(filter)
        

    def delete_filter(self, filter_name: str):
        """Filter 삭제 메서드"""
        if self.filter_manager.get_filter(filter_name):
            self.filter_manager.remove_filter(filter_name)

    def save_filter(self):
        self.filter_manager.save_filters()

    def load_filter(self):
        self.filter_manager.load_filters()

        
    def get_filter(self, filter_name):
        """Filter를 가져오게 하기"""
        return self.filter_manager.get_filter(filter_name)
    

    def update_filter(self, filter_target_name: str, filter_name: str, face_filter_on: bool, updated_face_filter: list, updated_object_filter: list):
        """Filter 업데이트 메서드"""
        if self.filter_manager.get_filter(filter_target_name):
            update_filter = Filter(filter_name, face_filter_on, updated_face_filter, updated_object_filter)
            self.filter_manager.update_filter(filter_target_name, update_filter)
            print(f"Filter '{filter_name}'의 face_filter 정보가 업데이트 되었습니다.")
        else:
            print(f"Filter '{filter_name}'를 찾을 수 없습니다.")


    def get_filters(self):
        """Filter """
        return self.filter_manager.get_filters()
