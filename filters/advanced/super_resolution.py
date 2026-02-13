# filters/advanced/super_resolution.py
import cv2
from filters.base_filter import BaseFilter


class SuperResolution(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Super-résolution (x2 Lanczos)"
        self.category = "Avancé / Amélioration"
        self.description = "Améliore la résolution de l'image par interpolation de haute qualité (algorithme Lanczos). Agrandit l'image sans perte visible de détails."

    def apply(self, image, params):
        scale = params.get("scale", 2.0)

        if scale <= 1.0 or scale == 1.0:
            # Pas de resize si scale = 1 (évite assertion failed)
            return image.copy()

        try:
            # Resize avec protection
            return cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)
        except cv2.error as e:
            print(f"Erreur resize SuperResolution (scale={scale}): {e}")
            return image.copy()  # Retourne original en cas d'erreur

    def get_default_params(self):
        return {"scale": 2.0}