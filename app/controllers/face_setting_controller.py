from models.face_manager import FaceManager
from controllers.path_finder import *
import pickle
import json

class PersonFaceSettingController:

    def __init__(self):
        self.test = ["person1", "person2", "person3"]
        self.face_list = []
        self.face_path = os.path.join(get_appdata_folder(), "mosaic")
        self.face_path = os.path.join(self.face_path, "face")
    
    def save_person_face(self, person: FaceManager):
        if not os.path.exists(self.face_path):
            os.makedirs(self.face_path)
        save_path = os.path.join(self.face_path, "register_note.bin")

        json_data = json.dumps([vars(fm) for fm in self.face_list])
        with open(save_path, 'wb') as file:
            file.write(pickle.dupms(json_data))

    def load_person_faces(self):
        if os.path.exists(self.face_path):
            save_path = os.path.join(self.face_path, "register_note.bin")
            with open(save_path, 'rb') as file:
                loaded_json_data = pickle.load(file)

            self.face_list = [FaceManager(**fm) for fm in json.loads(loaded_json_data)]

    def add_person_face(self, new_face: FaceManager):
        """person_face 추가 메서드"""
        names = []
        for face in self.face_list:
            names.append(face.face_name)
        if new_face not in names:  # 동일한 이름의 필터가 없는 경우에만 추가
            self.face_list.append(new_face)
        

    def delete_person_face(self, person_name: str):
        """person_face 삭제 메서드"""
        for face in self.face_list:
            if face.face_name == person_name:
                self.face_list.remove(face)
                break
        pass

        
    def get_person_face(self, person_name):
        """person_face를 가져오게 하기"""
        for face in self.face_list:
            if face.face_name == person_name:
                return face


    def update_person_face(self, person_name, person: FaceManager):
        """person_face 업데이트 메서드"""
        for face in self.face_list:
            if face.face_name == person_name:
                face.face_name = person.face_name
                face.encoding_list = person.encoding_list


    def get_person_faces(self):
        """person_face """
        return self.test[:]
