# filters/enhancement/bone_enhancement.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class BoneEnhancement(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Amélioration osseuse (médical)"
        self.category = "Amélioration médicale"
        self.description = "Renforce la visibilité des structures osseuses et des détails fins, particulièrement utile en radiographie."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        kernel = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(image, -1, kernel)
        return cv2.convertScaleAbs(sharpened)