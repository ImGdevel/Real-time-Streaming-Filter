import cv2
import dlib
import face_recognition

# 사람별 얼굴 특징을 저장하는 딕셔너리
known_faces = {}

# def recognize_face(known_faces, face_encoding):
#     min_distance = float('inf')
#     recognized_face = None
#     for name, encodings in known_faces.items():
#         for encoding in encodings:
#             distance = face_recognition.face_distance([encoding], face_encoding)
#             if distance < min_distance:
#                 min_distance = distance
#                 recognized_face = name/
#     return recognized_face

def recognize_face(known_faces, face_encoding, tolerance=0.5):
    recognized_face = "unknown"
    min_distance = float('inf')
    tolerance_used = None

    for name, encodings in known_faces.items():
        print(type(encodings))
        for encoding in encodings:
            print("Print")
            print(type(encoding))
            print(encoding)
            print("--------------------------------------")
            print(type(face_encoding))
            print(face_encoding)
            distance = face_recognition.face_distance([encoding], face_encoding)
            if distance < tolerance and distance < min_distance:
                min_distance = distance
                recognized_face = name
                tolerance_used = distance
                
    return recognized_face, tolerance_used

# 얼굴 특징을 추출하여 저장하는 함수
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
    person_faces = []
    for image_path in image_paths:
        face_features = extract_face_features(image_path)
        if face_features is not None:
            person_faces.append(face_features)
    if person_faces:
        known_faces[person_name] = person_faces

# 여러 장의 사진을 등록
register_person("SSH_glass", ["./tests/face_recognition/me_4.jpg"])
#register_person("WSH", ["./tests/face_recognition/WSH.png"])
#register_person("LJW", ["./tests/face_recognition/LJW.png"])
#register_person("SSH", ["./tests/face_recognition/me_left.jpg"])
#register_person("WSH2", ["./tests/face_recognition/WSH.png"])
#register_person("LJW2", ["./tests/face_recognition/LJW.png"])


# OpenCV를 사용하여 웹캠 열기
cap = cv2.VideoCapture(0)

while True:
    # 웹캠에서 프레임 읽기
    ret, frame = cap.read()
    
    # 프레임이 없으면 종료
    if not ret:
        break
    # 속도 향상을 위한 리사이징
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)

    # 얼굴 인식을 위해 dlib을 사용하여 얼굴 감지
    face_locations = face_recognition.face_locations(small_frame, model="cnn")

    # 감지된 얼굴들에 대해 반복
    for (top, right, bottom, left) in face_locations:
        # 리사이징된 스케일 업
        top *= 2; right *= 2; bottom *= 2; left *= 2
        
        # 각 얼굴 영역에서 얼굴 특징 추출
        
        face_encoding = face_recognition.face_encodings(frame, [(top, right, bottom, left)])[0]

        # 추출된 얼굴 특징을 등록된 얼굴과 비교하여 가장 유사한 얼굴 식별
        recognized_face, tolerance_used = recognize_face(known_faces, face_encoding)

        # 식별된 얼굴 이름을 화면에 표시
        text = recognized_face + " " + str(tolerance_used)
        #print(tolerance_used)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 화면에 프레임 표시
    cv2.imshow('Face Recognition', frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제 및 창 닫기
cap.release()
cv2.destroyAllWindows()
