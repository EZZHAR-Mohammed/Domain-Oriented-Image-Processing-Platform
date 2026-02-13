# filters/satellite/cloud_detection.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class CloudDetection(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Détection avancée de nuages"
        self.category = "Satellite / Prétraitement"
        self.description = "Détecte les nuages dans les images satellitaires en utilisant une combinaison de seuillage de couleur et de morphologie pour isoler les zones nuageuses, même dans des conditions d'éclairage variées."
    def apply(self, image, params):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_cloud = np.array([0, 0, 200])
        upper_cloud = np.array([180, 50, 255])
        mask = cv2.inRange(hsv, lower_cloud, upper_cloud)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        result = image.copy()
        result[mask > 0] = [100, 100, 255]  # Teinte bleue pour nuages
        return result

    def get_default_params(self):
        return {}