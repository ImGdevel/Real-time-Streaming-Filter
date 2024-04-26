import cv2
import numpy as np
import pickle
import os
from .path_manager import PathManager



class ReplaceManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.path_manager = PathManager()
    
    def register_img(self, img):
        """대체할 이미지를 등록 (imread시 알파채널까지 반드시 받아와야함 cv2.IMREAD_UNCHANGED)"""
        replace_images = self.path_manager.load_replace_images()
        max_img_number = -1
        for key in replace_images.keys():

            if key > max_img_number:
                max_img_number = key

        max_img_number += 1
        replace_images[max_img_number] = img

        self.path_manager.save_replace_images(replace_images)
        

    def load_img_to_id(self, img_id):
        replace_images = self.path_manager.load_replace_images()
        if img_id in replace_images:
            return replace_images[img_id]
    
    def delete_img(self, img_id):
        pass