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
        replace_images = self.path_manager.load_replace_images()
        max_img_number = -1
        for key in replace_images.keys():

            if key > max_img_number:
                max_img_number = key

        replace_images[key] = img

        self.path_manager.save_replace_images(replace_images)
        

    def load_img_to_id(self, img_id):
        replace_images = self.path_manager.load_replace_images()

        return replace_images[img_id]
    
    def delete_img(self, img_id):
        pass