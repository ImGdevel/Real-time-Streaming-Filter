import face_recognition
import cv2
import numpy as np

# 웹캠에서 라이브 비디오로 얼굴 인식을 실행하는 데모입니다. 기본 예제보다는 조금 더 복잡하지만 성능을 향상시키기 위한 몇 가지 기본적인 조정이 포함되어 있습니다:
#   1. 비디오 프레임을 1/4 해상도로 처리합니다(그러나 풀 해상도로 표시됩니다).
#   2. 비디오의 매 두 번째 프레임에서만 얼굴을 감지합니다.

# 주의: 이 예제는 웹캠에서 읽기 위해 OpenCV(`cv2` 라이브러리)가 설치되어 있어야 합니다.
# face_recognition 라이브러리를 사용하려면 OpenCV가 필요하지 않습니다. 이 특정 데모를 실행하려면 필요합니다.
# 설치에 문제가 있다면, 대신 필요하지 않는 다른 데모를 시도해 보세요.

# 웹캠 #0에 대한 참조를 가져옵니다(기본값).
video_capture = cv2.VideoCapture(0)

# 샘플 사진을 로드하고 인식하는 방법을 학습합니다.
obama_image = face_recognition.load_image_file("./obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# 두 번째 샘플 사진을 로드하고 인식하는 방법을 학습합니다.
biden_image = face_recognition.load_image_file("./biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# 알려진 얼굴 인코딩과 그들의 이름 배열을 만듭니다.
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "바라크 오바마",
    "조 바이든"
]

# 초기 변수를 설정합니다.
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # 비디오의 단일 프레임을 가져옵니다.
    ret, frame = video_capture.read()

    # 시간을 절약하기 위해 비디오의 매 두 번째 프레임만 처리합니다.
    if process_this_frame:
        # 빠른 얼굴 인식 처리를 위해 비디오 프레임의 크기를 1/4로 조정합니다.
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # OpenCV가 사용하는 BGR 색상에서 face_recognition이 사용하는 RGB 색상으로 이미지 변환합니다.
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # 현재 비디오 프레임에서 모든 얼굴과 얼굴 인코딩을 찾습니다.
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # 알려진 얼굴과 일치하는지 확인합니다.
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "알려지지 않은 사람"

            # 일치하는 얼굴 인코딩이 알려진 얼굴 인코딩 중 첫 번째 것만 사용합니다.
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # 결과를 표시합니다.
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # 검출된 프레임이 1/4 크기로 축소되었으므로 얼굴 위치를 다시 확대합니다.
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # 얼굴 주변에 박스를 그립니다.
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # 얼굴 아래에 이름 레이블을 그립니다.
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # 결과 이미지를 표시합니다.
    cv2.imshow('비디오', frame)

    # 키보드의 'q'를 눌러 종료합니다!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 웹캠 해제
video_capture.release()
cv2.destroyAllWindows()
