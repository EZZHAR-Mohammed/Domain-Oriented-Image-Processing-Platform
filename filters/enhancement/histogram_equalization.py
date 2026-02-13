# filters/enhancement/histogram_equalization.py
import cv2
from filters.base_filter import BaseFilter


class HistogramEqualization(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Égalisation d'histogramme"
        self.category = "Amélioration contraste"
        self.description = "Améliore le contraste global de l'image en redistribuant les intensités via égalisation d'histogramme."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        equalized = cv2.equalizeHist(gray)
        return cv2.cvtColor(equalized, cv2.COLOR_GRAY2BGR)