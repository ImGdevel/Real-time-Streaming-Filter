import os

def get_appdata_folder():
    # Windows 시스템에서만 작동
    if os.name == 'nt':
        # 환경 변수 'APPDATA'를 이용하여 AppData 폴더 경로 가져오기
        appdata_path = os.getenv('APPDATA')
        if appdata_path:
            return appdata_path
        else:
            # 환경 변수가 없는 경우, 일반적인 경로 조합 사용
            userprofile_path = os.getenv('USERPROFILE')
            if userprofile_path:
                return os.path.join(userprofile_path, 'AppData', 'Roaming')
            else:
                # USERPROFILE 변수도 없다면 경로를 찾을 수 없음
                return None
    else:
        # Windows 이외의 운영 체제에서는 지원하지 않음
        return None




def find_documents_folder():
    # Windows 시스템에서만 작동
    if os.name == 'nt':
        # 환경 변수 'USERPROFILE'를 이용하여 사용자 프로필 폴더 경로 가져오기
        userprofile_path = os.getenv('USERPROFILE')
        if userprofile_path:
            # Documents 폴더 경로 조합
            documents_path = os.path.join(userprofile_path, 'Documents')
            # Documents 폴더가 존재하는지 확인
            if os.path.exists(documents_path):
                return documents_path
            else:
                return None
        else:
            return None
    else:
        # Windows 이외의 운영 체제에서는 지원하지 않음
        return None

# # Documents 폴더 경로 가져오기
# documents_folder = find_documents_folder()

# if documents_folder:
#     print("사용자의 Documents 폴더:", documents_folder)
# else:
#     print("사용자의 Documents 폴더를 찾을 수 없습니다.")    
