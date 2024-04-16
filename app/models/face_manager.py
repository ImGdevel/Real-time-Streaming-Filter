from models.face_info import Face
import os
from controllers.path_finder import *
from models import FaceFilter
import pickle
import cv2
import numpy as np

class FaceManager:

    _instance = None
    face_list = []

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.face_path = os.path.join(get_appdata_folder(), "mosaic")
        self.face_path = os.path.join(self.face_path, "face")

    def save_person_face(self):
        """현재까지 변경된 사항들을 파일에 저장"""
        if not os.path.exists(self.face_path):
            os.makedirs(self.face_path)
        save_path = os.path.join(self.face_path, "register_note.bin")

        with open(save_path, 'wb') as file:
            pickle.dump(self.face_list, file)

    def load_person_faces(self):
        """기존에 등록된 face정보를 로드함"""
        if os.path.exists(self.face_path):
            save_path = os.path.join(self.face_path, "register_note.bin")
            with open(save_path, 'rb') as file:
                self.face_list = pickle.load(file)

        
    def add_person_face(self, new_face_name: str):
        """person_face 추가 메서드"""
        names = []
        for face in self.face_list:
            names.append(face.face_name)
        if new_face_name not in names:  # 동일한 이름의 필터가 없는 경우에만 추가
            self.face_list.append(FaceManager(new_face_name)) 

    def add_person_encoding(self, face_name: str, file_path):
        """face_name과 file_path를 전달하면 face_name과 일치하는 객체에 배열을 추가"""
        face_encoding = cv2.imread(file_path)
        FaceFilter.register_person(face_name, file_path)

        for face in self.face_list:
            if face.face_name == face_name:
                max_face_number = FaceFilter.find_max_face_number(face_name, face.encoding_list)
                max_face_number += 1
                face_code = face_name + "_" + str(max_face_number)
                face.encoding_list[face_code] = face_encoding
                

    def delete_person_face(self, person_name: str):
        """person_face 삭제 메서드"""
        for face in self.face_list:
            if face.face_name == person_name:
                self.face_list.remove(face)
                break
        pass

    def delete_person_encoding(self, person_name: str, encoding_name: str):
        """person_name의 encoding리스트 중 하나를 제거"""
        for face in self.face_list:
            if face.face_name == person_name:
                value = face.encoding_list.pop(encoding_name, 0)
                if value == 0:
                    print(f"'{encoding_name}'은 존재하지 않습니다.")
        
    def get_person_face(self, person_name):
        """person_face를 가져오게 하기"""
        for face in self.face_list:
            if face.face_name == person_name:
                return face
        print(f"'{person_name}이 존재하지 않습니다.'")

    def get_person_encoding(self, person_name: str, encoding_name: str):
        """person_name이 가진 encoding_name에 해당하는 numpy배열을 반환"""
        for face in self.face_list:
            if face.face_name == person_name:
                return face.encoding_list.get(encoding_name)
        print(f"'{person_name}이 존재하지 않습니다.'")
        return None
    
    def get_person_encodings(self, person_name: str):
        for face in self.face_list:
            if face.face_name == person_name:
                return face.encoding_list
        print(f"'{person_name}이 존재하지 않습니다.'")

    def update_person_face(self, person_name, person: Face):
        """person_face 업데이트 메서드"""
        for face in self.face_list:
            if face.face_name == person_name:
                face.face_name = person.face_name
                face.encoding_list = person.encoding_list

    def update_person_name(self, last_name: str, new_name: str):
        """사람 이름 변경"""
        for face in self.face_list:
            if face.face_name == new_name:
                return False
        for face in self.face_list:
            if face.face_name == last_name:
                face.face_name = new_name
                return True
            
        return False

    def get_person_faces(self):
        """person_face """
        return self.face_list


