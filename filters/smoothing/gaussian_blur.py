# filters/smoothing/gaussian_blur.py
import cv2
from filters.base_filter import BaseFilter
from typing import Dict, Any


class GaussianBlur(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Flou Gaussien"
        self.category = "Lissage / Réduction de bruit"
        self.description = "Applique un flou gaussien pour réduire le bruit"

    def apply(self, image: cv2.Mat, params: Dict[str, Any]) -> cv2.Mat:
        ksize = params.get("kernel_size", 5)
        sigma = params.get("sigma", 0)

        if ksize % 2 == 0:
            ksize += 1
        if ksize < 1:
            ksize = 1

        return cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma)

    def get_default_params(self) -> Dict[str, Any]:
        return {
            "kernel_size": 5,
            "sigma": 0.0
        }