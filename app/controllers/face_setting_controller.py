from models import FaceManager

class PersonFaceSettingController:

    def __init__(self):
        self.face_manager = FaceManager()
        self.load_person_faces()
    
    def save_person_face(self):
        """현재까지 변경된 사항들을 파일에 저장"""
        self.face_manager.save_person_face()

    def load_person_faces(self):
        """기존에 등록된 face정보를 로드함"""
        self.face_manager.load_person_faces()
    
    def add_person_face(self):
        """person_face 추가 메서드"""
        self.face_manager.add_person_face()

    def add_person_encoding_by_name(self, face_name: str, file_path):
        """face_name과 file_path를 전달하면 face_name과 일치하는 객체에 배열을 추가"""
        return self.face_manager.add_person_encoding_by_name_from_file(face_name, file_path)
    
    def add_person_encoding_by_name_from_img(self, face_name: str, img):
        return self.face_manager.add_person_encoding_by_name_from_img(face_name, img)

    def add_person_encoding_by_id(self, face_id: int, file_path):
        """face_name과 file_path를 전달하면 face_name과 일치하는 객체에 배열을 추가"""
        return self.face_manager.add_person_encoding_by_id(face_id, file_path)

    def delete_person_face_by_name(self, person_name: str):
        """person_face 삭제 메서드"""
        self.face_manager.delete_person_face_by_name(person_name)

    def delete_person_face_by_id(self, face_id: str):
        """person_face 삭제 메서드"""
        self.face_manager.delete_person_face_by_id(face_id)

    def delete_person_encoding_by_name(self, person_name: str, encoding_name: str):
        """person_name의 encoding리스트 중 하나를 제거"""
        self.face_manager.delete_person_encoding_by_name(person_name, encoding_name)

    def delete_person_encoding_by_id(self, face_id: int, encoding_name: str):
        """person_name의 encoding리스트 중 하나를 제거"""
        self.face_manager.delete_person_encoding_by_id(face_id, encoding_name)
        
    def get_person_face_by_name(self, person_name):
        """person_face를 가져오게 하기"""
        return self.face_manager.get_person_face_by_name(person_name)

    def get_person_face_by_id(self, face_id):
        """person_face를 가져오게 하기"""
        return self.face_manager.get_person_face_by_id(face_id)
    
    def get_person_face_name(self, face_id: int):
        return self.face_manager.get_person_face_name(face_id)
    
    def get_person_face_id(self, person_name: str):
        return self.face_manager.get_person_face_id(person_name)

    def get_person_encoding_by_name(self, person_name: str, encoding_name: str):
        """person_name이 가진 encoding_name에 해당하는 numpy배열을 반환"""
        return self.face_manager.get_person_encoding_by_name(person_name, encoding_name)
    
    def get_person_encoding_by_id(self, face_id: int, encoding_name: str):
        """face_id가 가진 encoding_name에 해당하는 numpy배열을 반환"""
        return self.face_manager.get_person_encoding_by_id(face_id, encoding_name)
    
    def get_person_encodings_by_name(self, person_name: str):
        """한 사람의 모든 인코딩 리스트 반환"""
        return self.face_manager.get_person_encodings_by_name(person_name)
    
    def get_person_encodings_by_id(self, face_id: int):
        """한 사람의 모든 인코딩 리스트 반환"""
        return self.face_manager.get_person_encodings_by_id(face_id)

    def get_person_faces(self):
        """person_face """
        return self.face_manager.get_person_faces()

    def update_person_name_by_name(self, last_name:str, new_name:str):
        """last_name을 new_name으로 변경"""
        if not self.face_manager.update_person_name_by_name(last_name, new_name):
            print("중복된 이름입니다.")
            return False    
        return True
    
    def update_person_name_by_id(self, face_id: int, new_name:str):
        """last_name을 new_name으로 변경"""
        if not self.face_manager.update_person_name_by_id(face_id, new_name):
            print("중복된 이름입니다.")
            return False    
        return True

    def update_person_face_by_name(self, person_name: str, person: dict):
        """person_face 업데이트 메서드"""
        self.face_manager.update_person_face_by_name(person_name, person)

    def update_person_face_by_id(self, face_id: int, person: dict):
        """person_face 업데이트 메서드"""
        self.face_manager.update_person_face_by_id(face_id, person)
