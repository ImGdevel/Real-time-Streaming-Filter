import dlib
import face_recognition
import re
import pickle
# 사람별 얼굴 특징을 저장하는 딕셔너리 가 필요함.. 다른 파일에 저장하도록
#known_faces = {}

# known_faces 딕셔너리 데이터를 저장된 파일에서부터 불러오는 함수
def load_known_faces(data_path):
    with open(data_path, 'rb') as f:
        loaded_data = pickle.load(f)

    return loaded_data


#frame내의 얼굴 위치를 받아 encoding 값을 반환
def face_encoding(frame, top, right, bottom, left):
    encoding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]
    return encoding


# "name" + _ + i 로 되어있는 딕셔너리에서 이름만 추출
def extract_name(name_i):
    matches = re.findall(r'(.+?)_\d+$', name_i)
    return matches[0]


#known_faces와 face_encoding 사이의 거리를 비교, tolerance 값 이하면 동일 인물로 간주 / 사람 이름과 tolerance 반환
def recognize_face(known_faces, face_encoding, tolerance=0.6):
    recognized_face = "unknown"
    min_distance = float('inf')
    tolerance_used = None
    
    for name, encodings in known_faces.items():
        for encoding in encodings:
            distance = face_recognition.face_distance([encoding], face_encoding)
            if distance < tolerance and distance < min_distance:
                min_distance = distance
                recognized_face = name
                tolerance_used = distance
                
    return recognized_face, tolerance_used




# 얼굴 특징을 추출하여 반환하는 함수 / 한 사진에 얼굴이 여러개 or 없으면 메시지 출력 후 None 반환
def extract_face_features(image_path):
    image = face_recognition.load_image_file(image_path)
    face_landmarks_list = face_recognition.face_landmarks(image)
    if len(face_landmarks_list) > 1:
        print("Too many faces in ", image_path)
        return None
    elif len(face_landmarks_list) > 0:
        return face_recognition.face_encodings(image)[0]
    else:
        print("Cannot found face in ", image_path)
        return None
    
# 사람의 여러 장의 사진을 등록하는 함수 
def register_person(person_name, image_paths):
    person_faces = {}
    i = 0
    for image_path in image_paths:
        face_features = extract_face_features(image_path)
        if face_features is not None:
            face_code = person_name + "_" + str(i)
            person_faces[face_code] = face_features #각 사진은 name_i : encoding 형태로 저장
            i = i + 1
    if person_faces:
        #known_faces[person_name] = person_faces // 이부분에는 파일에 쓰는 부분이 있어야할듯
        print(person_faces)
        with open('known_faces.pickle', 'wb') as f:
            pickle.dump(person_faces, f)

    else:
        print("아니 이사람 얼굴이 없는뎁쇼 : " + person_name)


#---------------------------------------------------------#
# import time

# start_time = time.time()

# test = "test"

# #register_person(test, ["./jlpt.jpg", "./jlpt2.jpg", "./WSH.png"])

# knoen_faces = load_known_faces('known_faces.pickle')

# # 로드된 데이터 확인
# print(knoen_faces)

# # 여기에 코드를 작성합니다.

# end_time = time.time()

# execution_time = end_time - start_time
# print("Execution time:", execution_time, "seconds")