import dlib
import face_recognition
import re
import pickle
# 사람별 얼굴 특징을 저장하는 딕셔너리 가 필요함.. 다른 파일에 저장하도록
#known_faces = {}

# 이미지에서 얼굴 특징을 추출하여 반환하는 함수
def extract_face_features(image_path):
    """
    주어진 이미지 파일에서 얼굴 특징을 추출합니다.
    
    Args:
    - image_path: 이미지 파일의 경로
    
    Returns:
    - 얼굴 특징을 나타내는 인코딩 값. 얼굴이 없는 경우 None을 반환합니다.
    """
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

# "name" + _ + i 로 되어있는 딕셔너리에서 이름만 추출하는 함수
def extract_name(name_i):
    """
    주어진 문자열에서 이름을 추출합니다.
    
    Args:
    - name_i: 이름과 인덱스가 결합된 문자열
    
    Returns:
    - 추출된 이름
    """
    matches = re.findall(r'(.+?)_\d+$', name_i)
    return matches[0]

# 사람별 얼굴 특징을 저장된 파일에서부터 불러오는 함수
def load_known_faces(data_path):
    """
    저장된 데이터 파일에서 사람별 얼굴 특징을 불러옵니다.
    
    Args:
    - data_path: 데이터 파일의 경로
    
    Returns:
    - 불러온 사람별 얼굴 특징을 나타내는 딕셔너리
    """
    with open(data_path, 'rb') as f:
        loaded_data = pickle.load(f)
    return loaded_data

# frame 내의 얼굴 위치를 받아 encoding 값을 반환하는 함수
def face_encoding(frame, top, right, bottom, left):
    """
    주어진 프레임에서 얼굴의 위치를 받아 인코딩 값을 반환합니다.
    
    Args:
    - frame: 이미지 프레임
    - top, right, bottom, left: 얼굴의 경계 상자 좌표
    
    Returns:
    - 얼굴의 인코딩 값
    """
    encoding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]
    return encoding

# 사람의 여러 장의 사진을 등록하는 함수
def register_person(person_name, image_paths):
    """
    사람의 여러 장의 사진을 등록하고 얼굴 특징을 저장합니다.
    
    Args:
    - person_name: 사람의 이름
    - image_paths: 사진 파일 경로의 리스트
    """
    person_faces = {}
    i = 0
    for image_path in image_paths:
        face_features = extract_face_features(image_path)
        if face_features is not None:
            face_code = person_name + "_" + str(i)
            person_faces[face_code] = face_features
            i = i + 1
    if person_faces:
        with open('known_faces.pickle', 'wb') as f:
            pickle.dump(person_faces, f)
    else:
        print("No faces found for :", person_name)

# known_faces와 face_encoding 사이의 거리를 비교하여 인식하는 함수
def recognize_face(known_faces, face_encoding, tolerance=0.6):
    """
    얼굴을 인식하여 인식된 사람과 일치하는지 확인합니다.
    
    Args:
    - known_faces: 사람별 얼굴 특징을 저장한 딕셔너리
    - face_encoding: 얼굴의 인코딩 값
    - tolerance: 허용 거리
    
    Returns:
    - 인식된 사람의 이름과 허용 거리
    """
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