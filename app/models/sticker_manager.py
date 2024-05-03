import cv2
import numpy as np
import pickle
import os
from .path_manager import PathManager
from PySide6.QtGui import QImage


class StickerManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.path_manager = PathManager()
    
    def register_img(self, img):
        """대체할 이미지를 등록 (imread시 알파채널까지 반드시 받아와야함 cv2.IMREAD_UNCHANGED)"""
        sticker_images = None
        sticker_images = self.path_manager.load_sticker_images()
        max_img_number = -1
        
        for key in sticker_images.keys():

            if key > max_img_number:
                max_img_number = key

        max_img_number += 1
        sticker_images[max_img_number] = img

        self.path_manager.save_sticker_images(sticker_images)

        return max_img_number
        
    def register_img_path(self, img_path):
        """대체할 이미지를 등록 (imread시 알파채널까지 반드시 받아와야함 cv2.IMREAD_UNCHANGED)"""
        sticker_images = None
        sticker_images = self.path_manager.load_sticker_images()
        max_img_number = -1

        for key in sticker_images.keys():

            if key > max_img_number:
                max_img_number = key

        max_img_number += 1
        sticker_images[max_img_number] = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

        self.path_manager.save_sticker_images(sticker_images)

        return max_img_number


    def load_img_to_id(self, img_id):
        sticker_images = self.path_manager.load_sticker_images()
        if img_id in sticker_images:
            return sticker_images[img_id]
    
    def load_Qimg_to_id(self, img_id):
        sticker_images = self.path_manager.load_sticker_images()
        if img_id in sticker_images:
            img = sticker_images[img_id]

            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR을 RGB로 변환
            height, width, channel = img.shape
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

            return q_img

    def delete_img(self, img_id):
        sticker_images = self.path_manager.load_sticker_images()

        if img_id in sticker_images:
            del sticker_images[img_id]
            self.path_manager.save_sticker_images(sticker_images)

            print(f"스티커 '{img_id}'가 삭제되었습니다.")
        else:
            print(f"스티커 '{img_id}'가 존재하지 않습니다.")
        

