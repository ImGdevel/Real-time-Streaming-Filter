
class PersonFaceSettingController:

    def __init__(self):
        self.test = ["person1", "person2", "person3"]
        

    def add_person_face(self, person_name: str):
        """person_face 추가 메서드"""
        if not self.get_person_face(person_name):  # 동일한 이름의 필터가 없는 경우에만 추가
            self.test.append(person_name)
        

    def delete_person_face(self, person_name: str):
        """person_face 삭제 메서드"""
        pass

        
    def get_person_face(self, person_name):
        """person_face를 가져오게 하기"""
        for person in self.test:
            if person == person_name:
                return person
    

    def update_person_face(self, person_name):
        """person_face 업데이트 메서드"""
        pass


    def get_person_faces(self):
        """person_face """
        return self.test[:]
