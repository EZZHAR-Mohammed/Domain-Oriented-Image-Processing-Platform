# core/image_manager.py
import cv2
import numpy as np

class ImageManager:
    def __init__(self):
        self.original_image = None
        self.current_image = None

    def load_image(self, file_path: str) -> bool:
        """Charge l'image depuis le chemin donné"""
        img = cv2.imread(file_path)
        if img is None:
            return False
        self.original_image = img.copy()
        self.current_image = img.copy()
        return True

    def get_current(self) -> np.ndarray | None:
        """Retourne l'image courante (celle affichée/modifiée)"""
        return self.current_image

    def get_original(self) -> np.ndarray | None:
        """Retourne l'image originale chargée"""
        return self.original_image

    def set_current(self, img: np.ndarray):
        """Met à jour l'image courante"""
        self.current_image = img

    def update_current(self, new_img):
        self.set_current(new_img)  # si tu as déjà set_current

    def reset_to_original(self) -> None:
        """Réinitialise l'image courante à l'originale"""
        if self.original_image is not None:
            self.current_image = self.original_image.copy()
        else:
            print("Aucune image originale chargée → reset ignoré")

    def save_current(self, file_path: str) -> bool:
        """Sauvegarde l'image courante"""
        if self.current_image is None:
            return False
        return cv2.imwrite(file_path, self.current_image)