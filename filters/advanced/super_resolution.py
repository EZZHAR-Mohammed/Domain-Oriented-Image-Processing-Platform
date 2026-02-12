# filters/advanced/super_resolution.py
import cv2
from filters.base_filter import BaseFilter


class SuperResolution(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Super-résolution (x2 Lanczos)"
        self.category = "Avancé / Amélioration"
        self.description = "Améliore la résolution par interpolation de haute qualité"

    def apply(self, image, params):
        scale = params.get("scale", 2)
        return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)

    def get_default_params(self):
        return {"scale": 2}