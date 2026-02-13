# filters/enhancement/terrain_enhancement.py
import cv2
from filters.base_filter import BaseFilter


class TerrainEnhancement(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Amélioration terrain (Sobel)"
        self.category = "Satellite / Géographie"
        self.description = "Renforce les détails topographiques et les structures de terrain en utilisant l'opérateur de Sobel pour détecter les contours et les reliefs."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)
        sobel = cv2.magnitude(sobelx, sobely)
        sobel = cv2.convertScaleAbs(sobel)
        return cv2.cvtColor(sobel, cv2.COLOR_GRAY2BGR)