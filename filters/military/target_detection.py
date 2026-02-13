# filters/military/target_detection.py
import cv2
from filters.base_filter import BaseFilter


class TargetDetection(BaseFilter):
    """
    Détection de cibles adaptative pour imagerie militaire
    Utilise un seuillage adaptatif + dessin de contours
    """
    def __init__(self):
        super().__init__()
        self.name = "Détection de cibles adaptative"
        self.category = "Militaire / Reconnaissance"
        self.description = "Détection de cibles adaptative pour imagerie militaire. Utilise un seuillage adaptatif pour identifier les zones d'intérêt et dessine des contours autour des cibles potentielles."
    def apply(self, image, params):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            11, 2
        )
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = image.copy()
        cv2.drawContours(result, contours, -1, (0, 255, 255), 2)  # Jaune vif pour visibilité
        return result

    def get_default_params(self):
        return {}