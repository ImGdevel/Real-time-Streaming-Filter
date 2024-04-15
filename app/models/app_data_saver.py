import os
import pickle
import ctypes

class AppDataSaver:
    '''앱 데이터를 저장하고 불러오는 클래스'''
    def __init__(self, data):
        # 초기화 메서드
        self.data = data
        # 앱 데이터 폴더 경로를 가져옴
        self.appdata_path = os.getenv('APPDATA')
        # RSF 폴더 경로 설정
        self.rsf_folder_path = os.path.join(self.appdata_path, 'RSF')
        
        # RSF 폴더가 없으면 생성
        if not os.path.exists(self.rsf_folder_path):
            os.makedirs(self.rsf_folder_path)

    def save_data(self, filename):
        '''데이터를 파일에 저장하는 메서드'''
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        file_path = os.path.join(self.rsf_folder_path, filename)
        with open(file_path, 'wb') as file:
            pickle.dump(self.data, file)
        print(f"App data saved to {file_path}")

    def load_data(self, filename):
        '''파일에서 데이터를 불러오는 메서드'''
        if not filename.endswith('.pkl'):
            filename += '.pkl'
        file_path = os.path.join(self.rsf_folder_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                loaded_data = pickle.load(file)
            print(f"App data loaded from {file_path}")
            return loaded_data
        else:
            print(f"{file_path} does not exist.")
            return None