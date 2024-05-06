from models.path_finder import *
import pickle

class PathManager:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.base_path = os.path.join(get_appdata_folder(), "mosaic")
        
        self.face_file = os.path.join(self.base_path, "face_data.bin")
        self.setting_file = os.path.join(self.base_path, "setting_data.bin")
        self.filter_file = os.path.join(self.base_path, "filter_data.bin")
        self.known_faces = os.path.join(self.base_path, "known_faces.pickle")
        self.sticker_images = os.path.join(self.base_path, "sticker_images.bin")
        self.tempdata_dir = os.path.join(self.base_path, "TempData/")

        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)

    def save_face_data(self, face_data):
        """face 정보를 파일에 저장"""
        with open(self.face_file, 'wb') as file:
            pickle.dump(face_data, file)
        pass

    def save_setting_data(self, setting_data):
        """setting 정보를 파일에 저장"""
        with open(self.setting_file, 'wb') as file:
            pickle.dump(setting_data, file)

    def save_filter_data(self, filter_data):
        """filter 정보를 파일에 저장"""
        with open(self.filter_file, 'wb') as file:
            pickle.dump(filter_data, file)

    def save_sticker_images(self, images):
        """대체 이미지를 저장"""
        with open(self.sticker_images, 'wb') as file:
            pickle.dump(images, file)

    def load_face_data(self):
        """기존에 등록된 face정보를 로드함"""
        if os.path.exists(self.face_file):
            with open(self.face_file, 'rb') as file:
                face_data = pickle.load(file)
            return face_data
        else:
            return []

    def load_setting_data(self):
        """기존에 등록된 setting정보를 로드함"""
        if os.path.exists(self.setting_file):
            with open(self.setting_file, 'rb') as file:
                setting_data = pickle.load(file)
            return setting_data
        else:
            return []      

    def load_filter_data(self):
        """기존에 등록된 filter정보를 로드함"""
        if os.path.exists(self.filter_file):
            with open(self.filter_file, 'rb') as file:
                filter_data = pickle.load(file)
            return filter_data
        else:
            return []


    def load_sticker_images(self):
        if os.path.exists(self.sticker_images):
            with open(self.sticker_images, 'rb') as file:
                replace_images = pickle.load(file)
            return replace_images
        else:
            return {}

    def load_download_path(self):
        """임시 download_path 불러옴 (documents)"""
        documents_folder = find_documents_folder()
        if documents_folder:
            # Documents 폴더 내에 임시 다운로드 폴더 생성
            download_folder = os.path.join(documents_folder, 'TempDownloads')
            # TempDownloads 폴더가 없으면 생성
            if not os.path.exists(download_folder):
                os.makedirs(download_folder)
                print("TempDownloads 폴더를 생성했습니다.")
            return download_folder
        else:
            print("Documents 폴더를 찾을 수 없습니다.")
            return None
        
    def load_TempData_path(self):
        """임시 TempData_path 불러옴 (appdata)"""
        appdata_folder = get_appdata_folder()
        if appdata_folder:
           
            tempdata_folder = os.path.join(appdata_folder, 'mosaic/TempData')
            
            if not os.path.exists(tempdata_folder):
                os.makedirs(tempdata_folder)
                print("tempdata_folder 폴더를 생성했습니다.")
            return tempdata_folder
        else:
            print("Documents 폴더를 찾을 수 없습니다.")
            return None

    def load_known_faces_path(self):
        """known_faces.pickle 경로"""
        return self.known_faces
