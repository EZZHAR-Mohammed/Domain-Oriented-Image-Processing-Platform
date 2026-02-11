import cv2
import numpy as np

class ImageManager:
    def __init__(self):
        self.original_image = None
        self.current_image = None
        self.filename = None

    def load_image(self, path):
        img = cv2.imread(path)
        if img is None:
            return False
        self.original_image = img.copy()
        self.current_image = img.copy()
        self.filename = path
        return True

    def get_current(self):
        return self.current_image

    def get_original(self):
        return self.original_image

    def update_current(self, new_img):
        self.current_image = new_img

    def reset_to_original(self):
        if self.original_image is not None:
            self.current_image = self.original_image.copy()

    def save_current(self, path):
        if self.current_image is not None:
            cv2.imwrite(path, self.current_image)
            return True
        return False