from .face_info import Face
from .FaceFilter import *
import cv2
import numpy as np
from .path_manager import PathManager
from PySide6.QtGui import QImage
from .filter_manager import FilterManager

class FaceManager:

    _instance = None
    face_list : list[Face] = []
    filter_manager = FilterManager()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        self.path_manager = PathManager()

    def save_person_face(self):
        """현재까지 변경된 사항들을 파일에 저장"""
        self.path_manager.save_face_data(self.face_list)

    def load_person_faces(self):
        """기존에 등록된 face정보를 로드함"""
        self.face_list = self.path_manager.load_face_data()

    def add_person_face(self):
        """person_face 추가 메서드"""
        names = []
        max_face_id = -1
        index = 1
        for face in self.face_list:
            names.append(face.face_name)
            if max_face_id < face.face_id:
                max_face_id = face.face_id
            
        name = "사람" + str(index)
        while True:
            if name in names:
                index += 1
                name = "사람" + str(index)
            else:
                break
        max_face_id += 1
        self.face_list.append(Face(max_face_id, name)) 
        self.save_person_face()


    def add_person_encoding_by_name(self, face_name: str, image: np.ndarray):
        """face_name과 image를 전달하면 face_name과 일치하는 객체에 배열을 추가"""
        # if qimage.format() != QImage.Format_ARGB32:
        #     # QImage를 32비트 이미지로 변환
        #     qimage = qimage.convertToFormat(QImage.Format_ARGB32)

        # image = qimage2ndarray.rgb_view(qimage)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        for face in self.face_list:
            if face.face_name == face_name:
                if  register_person(str(face.face_id), image, self.path_manager.load_known_faces_path()):
                    max_face_number = find_max_face_number(face_name, face.encoding_list)
                    max_face_number += 1
                    face_code = face_name + "_" + str(max_face_number)
                    face.encoding_list[face_code] = image
                    self.save_person_face()
                    return True
                else:
                    raise Exception("face error")
                
        raise ValueError("face name error")   
    
    # def add_person_encoding_by_name_from_img(self, face_name: str, img):
    #     for face in self.face_list:
    #         print("face.face_name", face.face_name)
    #         print("face_name",face_name)
    #         if face.face_name == face_name:
    #             if  register_person_by_img(str(face.face_id), img, self.path_manager.load_known_faces_path()):
    #                 max_face_number = find_max_face_number(face_name, face.encoding_list)
    #                 max_face_number += 1
    #                 face_code = face_name + "_" + str(max_face_number)
    #                 face.encoding_list[face_code] = img
    #                 self.save_person_face()
    #                 return True
                
        # raise ValueError("존재하지 않는 face_name입니다")

    def add_person_encoding_by_id(self, face_id: int, image: np.ndarray):
        """face_name과 file_path를 전달하면 face_name과 일치하는 객체에 배열을 추가"""
        # if qimage.format() != QImage.Format_ARGB32:
        #     # QImage를 32비트 이미지로 변환
        #     qimage = qimage.convertToFormat(QImage.Format_ARGB32)

        # image = qimage2ndarray.rgb_view(qimage)
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        for face in self.face_list:
            if face.face_id == face_id:
                if  register_person(str(face.face_id), image, self.path_manager.load_known_faces_path()):
                    max_face_number = find_max_face_number(face_id, face.encoding_list)
                    max_face_number += 1
                    face_code = face_id + "_" + str(max_face_number)
                    face.encoding_list[face_code] = image
                    self.save_person_face()
                    return True
                
        raise ValueError("존재하지 않는 face_id입니다")

    def delete_person_face_by_name(self, person_name: str):
        """person_face 삭제 메서드"""
        #print("delete person face")
        for face in self.face_list:
            if face.face_name == person_name:
                self.face_list.remove(face)
                for filter in self.filter_manager.filter_list:
                    self.filter_manager.delete_face_in_filter(filter.name, face.face_id)
                self.save_person_face()
                return True
        raise ValueError("존재하지 않는 face_name입니다")

    def delete_person_face_by_id(self, face_id: int):
        """person_face 삭제 메서드"""
        #print("delete person face")
        for face in self.face_list:
            if face.face_id == face_id:
                self.face_list.remove(face)
                for filter in self.filter_manager.filter_list:
                    self.filter_manager.delete_face_in_filter(filter.name, face_id)
                self.save_person_face()
                return True
        raise ValueError("존재하지 않는 face_id입니다")

    def delete_person_encoding_by_name(self, person_name: str, encoding_name: str):
        """person_name의 encoding리스트 중 하나를 제거"""
        #print("delete person encoding")
        for face in self.face_list:
            if face.face_name == person_name:
                value = face.encoding_list.pop(encoding_name, 0)
                if value != 0:
                    self.save_person_face()
                    return True
                else:
                    raise ValueError("존재하지 않는 encoding_name입니다")

        raise ValueError("존재하지 않는 face_name입니다")

    def delete_person_encoding_by_id(self, face_id: str, encoding_name: str):
        """person_name의 encoding리스트 중 하나를 제거"""
        #print("delete person encoding")
        for face in self.face_list:
            if face.face_id == face_id:
                value = face.encoding_list.pop(encoding_name, 0)
                if value != 0:
                    self.save_person_face()
                    return True
                else:
                    raise ValueError("존재하지 않는 encoding_name입니다")

        raise ValueError("존재하지 않는 face_id입니다")
        
    def get_person_face_by_name(self, person_name):
        """person_face를 가져오게 하기"""
        #print("get person face")
        for face in self.face_list:
            if face.face_name == person_name:
                return face
        raise ValueError("존재하지 않는 face_name입니다")

    def get_person_face_by_id(self, face_id : int):
        """person_face를 가져오게 하기"""
        #print("get person face")
        for face in self.face_list:
            if face.face_id == face_id:
                return face
        return None

    def get_person_face_name(self, face_id : int):
        for face in self.face_list:
            if face.face_id == face_id:
                return face.face_name
        return None

    def get_person_face_id(self, person_name):
        """person_face_id를 가져오게 하기"""
        for face in self.face_list:
            if face.face_name == person_name:
                return face.face_id
        raise ValueError("존재하지 않는 face_name입니다")

    def get_person_encoding_by_name(self, person_name: str, encoding_name: str) -> QImage:
        """person_name이 가진 encoding_name에 해당하는 numpy배열을 반환"""
        #print("get person encoding")
        for face in self.face_list:
            if face.face_name == person_name:
                face_encoding = face.encoding_list.get(encoding_name)
                face_encoding = cv2.cvtColor(face_encoding, cv2.COLOR_BGR2RGB)
                height, width, channel = face_encoding.shape
                bytes_per_line = 3 * width
                q_image = QImage(face_encoding.data, width, height, bytes_per_line, QImage.Format_RGB888)
                
                return q_image
        raise ValueError("존재하지 않는 face_name입니다")


    def get_person_encoding_by_id(self, face_id: int, encoding_name: str) -> QImage:
        """person_name이 가진 encoding_name에 해당하는 numpy배열을 반환"""
        #print("get person encoding")
        for face in self.face_list:
            if face.face_id == face_id:
                face_encoding = face.encoding_list.get(encoding_name)
                face_encoding = cv2.cvtColor(face_encoding, cv2.COLOR_BGR2RGB)
                height, width, channel = face_encoding.shape
                bytes_per_line = 3 * width
                q_image = QImage(face_encoding.data, width, height, bytes_per_line, QImage.Format_RGB888)
                
                return q_image
        raise ValueError("존재하지 않는 face_id입니다")


    def get_person_encodings_by_name(self, person_name: str):
        #print("get person encodings")
        for face in self.face_list:
            if face.face_name == person_name:
                q_images = []
                for face_encoding in face.encoding_list.values():
                    face_encoding = cv2.cvtColor(face_encoding, cv2.COLOR_BGR2RGB)
                    height, width, channel = face_encoding.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(face_encoding.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    q_images.append(q_image)
                return q_images
        return None

    def get_person_encodings_by_id(self, face_id: int):
        #print("get person encodings")
        for face in self.face_list:
            if face.face_id == face_id:
                q_images = []
                for face_encoding in face.encoding_list.values():
                    face_encoding = cv2.cvtColor(face_encoding, cv2.COLOR_BGR2RGB)
                    height, width, channel = face_encoding.shape
                    bytes_per_line = 3 * width
                    q_image = QImage(face_encoding.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    q_images.append(q_image)
                return q_images
        raise ValueError("존재하지 않는 face_id입니다")

    def get_person_faces(self):
        """person_face """
        #print("get person faces")
        return self.face_list
    
    def update_person_face_by_name(self, person_name, person: dict):
        """person_face 업데이트 메서드"""
        for face in self.face_list:
            if face.face_name == person_name:
                face.encoding_list = person
                self.save_person_face()
                return True
        raise ValueError("존재하지 않는 face_name입니다")
        

    def update_person_face_by_id(self, face_id: int, person: dict):
        """person_face 업데이트 메서드"""
        for face in self.face_list:
            if face.face_id == face_id:
                face.encoding_list = person
                self.save_person_face()
                return True
        raise ValueError("존재하지 않는 face_id입니다")


    def update_person_name_by_name(self, last_name: str, new_name: str):
        """사람 이름 변경"""
        #print("update person name")
        for face in self.face_list:
            if face.face_name == new_name:
                return False
        for face in self.face_list:
            if face.face_name == last_name:
                face.face_name = new_name
                self.save_person_face()
                return True
        return False

    
    def update_person_name_by_id(self, face_id: int, new_name: str):
        """사람 이름 변경"""
        #print("update person name")
        for face in self.face_list:
            if face.face_name == new_name:
                raise ValueError("중복된 이름입니다")

        for face in self.face_list:
            if face.face_id == face_id:
                face.face_name = new_name
                self.save_person_face()
                return True
            
        raise ValueError("존재하지 않는 face_id입니다")



