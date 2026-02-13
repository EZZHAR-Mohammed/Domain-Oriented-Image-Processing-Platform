# filters/enhancement/thermal_enhancement.py
import cv2
from filters.base_filter import BaseFilter


class ThermalEnhancement(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Amélioration thermique (color mapping)"
        self.category = "Militaire / Thermique"
        self.description = "Améliore les images thermiques en appliquant une carte de couleurs (colormap) pour mieux visualiser les différences de température et les détails thermiques."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        colored = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
        return colored