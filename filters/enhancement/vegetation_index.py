# filters/enhancement/vegetation_index.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class VegetationIndex(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Indice de végétation (NDVI-like)"
        self.category = "Satellite / Agriculture"
        self.description = "Calcule un indice de végétation similaire au NDVI en utilisant les canaux rouge et bleu pour mettre en évidence la végétation dans les images aériennes ou satellitaires."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        b, g, r = cv2.split(image.astype(np.float32))
        ndvi = (r - b) / (r + b + 1e-6)
        ndvi = np.clip((ndvi + 1) * 127.5, 0, 255).astype(np.uint8)
        return cv2.applyColorMap(ndvi, cv2.COLORMAP_VIRIDIS)