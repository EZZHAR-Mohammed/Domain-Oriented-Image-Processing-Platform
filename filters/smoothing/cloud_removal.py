# filters/smoothing/cloud_removal.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter
from typing import Dict, Any


class CloudRemoval(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Suppression de nuages (simple)"
        self.category = "Lissage / Satellite"
        self.description = "Masque et remplace les zones claires (nuages) par une valeur moyenne"

    def apply(self, image: cv2.Mat, params: Dict[str, Any]) -> cv2.Mat:
        threshold = params.get("threshold", 220)
        replace_value = params.get("replace_value", 100)

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, (0, 0, threshold), (180, 30, 255))

        result = image.copy()
        result[mask > 0] = replace_value

        return result

    def get_default_params(self) -> Dict[str, Any]:
        return {
            "threshold": 220,
            "replace_value": 100
        }