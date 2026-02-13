# filters/morphology/erosion.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class Erosion(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Érosion morphologique"
        self.category = "Morphologie"
        self.description = "Applique une érosion morphologique pour réduire les objets dans l'image. Utile pour éliminer le bruit ou séparer des objets connectés."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        kernel_size = params.get("kernel_size", 3)
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        eroded = cv2.erode(gray, kernel, iterations=1)
        return cv2.cvtColor(eroded, cv2.COLOR_GRAY2BGR)