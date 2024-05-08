import cv2
import os
import numpy as np
from datetime import datetime
from models import Filtering, PathManager, FilterManager
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication
import qimage2ndarray


# 비디오 처리 스레드
class ImageProcessor():

    def __init__(self):
        super().__init__()
        self.filtering = Filtering()
        self.path_manager = PathManager()
        self.filter_manager = FilterManager()


    #원본 사진을 받아서 임시로 이미지 처리
    def filtering_images(self, image_paths):
        processed_images = []
        for image_path in image_paths:
            # 이미지 읽어오기
            image = cv2.imread(image_path)
            
            # 이미지 처리 
            #blur_ratio = 50

            boxesList = self.filtering.filtering(image)
            processed_image = self.filtering.square_blur(image, boxesList)
            

            
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            height, width, channel = processed_image.shape
            bytes_per_line = 3 * width
            q_img = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            processed_images.append(q_img)

        return processed_images

    #원본 사진을 받아서 임시로 이미지 처리
    def filtering_images_to_dict(self, image_paths, progress_dialog):
        total_elements = len(image_paths)
        processed_images_dict = {}
        for i, image_path in enumerate(image_paths):
            #다이얼로그 처리
            progress = ((i + 1) / total_elements) * 100
            progress_dialog.setValue(progress)
            QApplication.processEvents()
            if progress_dialog.wasCanceled():
                return dict()
            # 이미지 읽어오기
            image = cv2.imread(image_path)
            
            # 이미지 처리 
            blur_ratio = 50

            boxesList = self.filtering.filtering(image)
            for key in boxesList.keys():
                if key == -1:
                    if boxesList[key] is not None:
                        processed_image = self.filtering.blur(image, boxesList[key])
                elif key == -2:
                    if boxesList[key] is not None:
                        processed_image = self.filtering.square_blur(image, boxesList[key])
                else:
                    if boxesList[key] is not None:
                        processed_image = self.filtering.face_sticker(image, boxesList[key], key)
            
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            height, width, channel = processed_image.shape
            bytes_per_line = 3 * width
            q_img = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            processed_images_dict[image_path] = q_img


        return processed_images_dict


    def create_filtered_image(self, QImage_list):
        """
        QImage 객체의 리스트를 받아 처리된 이미지를 파일로 저장합니다.

        Args:
        - QImage_list: 처리할 QImage 객체들의 리스트
        """
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        download_directory = self.path_manager.load_download_path()
        print("down images to : " + download_directory)
        sequence_number = 1
        for qimage in QImage_list:
            img = self.QImage_to_cv2(qimage)
            #img = qimage2ndarray.rgb_view(qimage)

            # # 처리된 이미지를 파일로 저장 (새로운 파일명을 만듦)
            image_name = f"{current_time}_{sequence_number}.jpg"
            output_path = os.path.join(download_directory, image_name)
            cv2.imwrite(output_path, img)
            # print(f"이미지 처리 및 저장 완료: {output_path}")
            sequence_number += 1


    def create_filtered_image_dict(self, QImage_dict):
        """
        QImage 객체의 딕셔너리를 받아 처리된 이미지를 파일로 저장합니다.

        Args:
        - QImage_dict: 처리할 QImage 객체들의 딕셔너리
        """
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        download_directory = self.path_manager.load_download_path()
        print("down images to : " + download_directory)
        sequence_number = 1
        for key, qimage in QImage_dict.items():

            if qimage.format() != QImage.Format_ARGB32:
                # QImage를 32비트 이미지로 변환
                qimage = qimage.convertToFormat(QImage.Format_ARGB32)

            img = qimage2ndarray.rgb_view(qimage)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # # 처리된 이미지를 파일로 저장 (새로운 파일명을 만듦)
            image_name = f"{current_time}_{sequence_number}.jpg"
            output_path = os.path.join(download_directory, image_name)
            cv2.imwrite(output_path, img)
            # print(f"이미지 처리 및 저장 완료: {output_path}")
            sequence_number += 1

    def set_filter(self, filter):
        """
        필터 설정
        
        Args:
        - filter: 설정할 필터
        """
        if not filter is None:
            current_filter = self.filter_manager.get_filter(filter)
            print("현제 적용 필터 :",  current_filter)
            self.filtering.set_filter(current_filter)

            






    # 이미지를 OpenCV 형식으로 변환하는 메소드
    def QImage_to_cv2(self, qimage):
        if qimage.format() != QImage.Format_RGB888:
            # QImage의 형식이 RGB888이 아니면 변환
            qimage = qimage.convertToFormat(QImage.Format_RGB888)
        
        width = qimage.width()
        height = qimage.height()
        
        # QImage에서 데이터를 가져와서 numpy 배열로 변환
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        arr = np.array(ptr).reshape(height, width, 3)  # 3 channels for RGB
        
        # OpenCV의 BGR 형식으로 변환
        cv_img = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        
        return cv_img



    # def QImage_to_cv2(self, qimage):
    #     """
    #     QImage를 numpy 배열로 변환합니다.
        
    #     Args:
    #     - qimage: 변환할 QImage 객체
        
    #     Returns:
    #     - 변환된 numpy 배열
    #     """
    #     width = qimage.width()
    #     height = qimage.height()
    #     byte_per_line = qimage.bytesPerLine()
    #     image_format = qimage.format()
  
    #     # QImage를 numpy 배열로 변환
    #     ptr = qimage.constBits()
    #     ptr.setsize(qimage.byteCount())
    #     img_arr = np.array(ptr).reshape(height, width, -1)

    #     return img_arr