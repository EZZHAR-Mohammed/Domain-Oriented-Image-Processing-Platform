# filters/enhancement/stain_enhancement.py
import cv2
from filters.base_filter import BaseFilter


class StainEnhancement(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Amélioration des colorations (biologie)"
        self.category = "Biologie / Microscopie"

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = cv2.multiply(hsv[:,:,1], 1.4)  # boost saturation
        return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)