import cv2
import os
import numpy as np
from datetime import datetime
from models import Filtering, PathManager, FilterManager
from PySide6.QtGui import QImage
from PySide6.QtWidgets import QApplication



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
            processed_image = self.filtering.blur(image, boxesList)
            

            
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
            processed_image = self.filtering.blur(image, boxesList)
            

            
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            height, width, channel = processed_image.shape
            bytes_per_line = 3 * width
            q_img = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

            processed_images_dict[image_path] = q_img


        return processed_images_dict

    def QImage_to_cv2(qimage):
        """
        QImage를 numpy 배열로 변환합니다.
        
        Args:
        - qimage: 변환할 QImage 객체
        
        Returns:
        - 변환된 numpy 배열
        """
        width = qimage.width()
        height = qimage.height()
        byte_per_line = qimage.bytesPerLine()
        image_format = qimage.format()

        # QImage를 numpy 배열로 변환
        ptr = qimage.constBits()
        ptr.setsize(qimage.byteCount())
        img_arr = np.array(ptr).reshape(height, width, int(byte_per_line / height))

        return img_arr


    def create_filtered_image(self, QImage_list):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        download_directory = self.path_manager.load_download_path()
        print("down images to : " + self.output_video_path)
        sequence_number = 1
        for qimage in QImage_list:
            img = self.QImage_to_cv2(qimage)
            # # 처리된 이미지를 파일로 저장 (새로운 파일명을 만듦)
            image_name = f"{current_time}_{sequence_number}.jpg"
            output_path = os.path.join(download_directory, image_name)
            cv2.imwrite(output_path, img)
            # print(f"이미지 처리 및 저장 완료: {output_path}")
            sequence_number += 1

    def create_filtered_image_dict(self, QImage_dict):
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        download_directory = self.path_manager.load_download_path()
        print("down images to : " + self.output_video_path)
        sequence_number = 1
        for key, qimage in QImage_dict.items():
            img = self.QImage_to_cv2(qimage)
            # # 처리된 이미지를 파일로 저장 (새로운 파일명을 만듦)
            image_name = f"{current_time}_{sequence_number}.jpg"
            output_path = os.path.join(download_directory, image_name)
            cv2.imwrite(output_path, img)
            # print(f"이미지 처리 및 저장 완료: {output_path}")
            sequence_number += 1

    def set_filter(self, filter):
        """필터 설정"""
        if not filter is None:
            current_filter = self.filter_manager.get_filter(filter)
            print("현제 적용 필터 :",  current_filter)
            self.filtering.set_filter(current_filter)

            