# core/image_manager.py
import cv2
import numpy as np

class ImageManager:
    def __init__(self):
        self.original_image = None
        self.current_image = None

    def load_image(self, file_path):
        img = cv2.imread(file_path)
        if img is None:
            return False
        self.original_image = img.copy()
        self.current_image = img.copy()
        return True

    def get_image(self):
        """Retourne l'image courante (celle affichée/modifiée)"""
        return self.current_image

    def get_original_image(self):
        return self.original_image

    def set_image(self, img):
        self.current_image = img

    def reset_to_original(self):
        """Méthode qui manquait → cause de l'erreur actuelle"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
        else:
            print("Aucune image originale → reset ignoré")

    def save_image(self, file_path):
        if self.current_image is not None:
            return cv2.imwrite(file_path, self.current_image)
        return False