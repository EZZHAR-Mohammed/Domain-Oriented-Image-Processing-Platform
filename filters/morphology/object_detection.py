# filters/morphology/object_detection.py
import cv2
from filters.base_filter import BaseFilter


class ObjectDetection(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Détection d'objets simple (contours)"
        self.category = "Morphologie / Détection"
        self.description = "Détecte les objets dans l'image en utilisant la détection de contours. Utile pour identifier et localiser des objets distincts dans une scène."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = image.copy()
        cv2.drawContours(result, contours, -1, (0, 255, 0), 2)
        return result