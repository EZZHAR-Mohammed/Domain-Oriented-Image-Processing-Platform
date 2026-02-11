# filters/enhancement/contrast_enhancement.py
import cv2
from filters.base_filter import BaseFilter


class ContrastEnhancement(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Amélioration de contraste (CLAHE)"
        self.category = "Amélioration contraste"
        self.description = "CLAHE – contraste local adaptatif"

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        lab[:,:,0] = clahe.apply(lab[:,:,0])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)