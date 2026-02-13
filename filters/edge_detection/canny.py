# filters/edge_detection/canny.py
import cv2
from filters.base_filter import BaseFilter
from typing import Dict, Any


class CannyEdge(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Détection de contours – Canny"
        self.category = "Détection de bords"
        self.description = "Utilise l'algorithme Canny classique pour détecter les contours et les bords principaux de l'image."

    def apply(self, image: cv2.Mat, params: Dict[str, Any]) -> cv2.Mat:
        low = params.get("low_threshold", 50)
        high = params.get("high_threshold", 150)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low, high)

        # Retourner en 3 canaux pour affichage cohérent
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    def get_default_params(self) -> Dict[str, Any]:
        return {
            "low_threshold": 50,
            "high_threshold": 150
        }