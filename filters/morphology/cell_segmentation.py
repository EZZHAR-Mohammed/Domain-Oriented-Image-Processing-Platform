# filters/morphology/cell_segmentation.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class CellSegmentation(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Segmentation cellulaire (Watershed simplifié)"
        self.category = "Biologie / Segmentation"
        self.description = "Segmente les cellules ou objets dans une image biologique en utilisant une approche simplifiée de l'algorithme de Watershed. Utile pour l'analyse de cultures cellulaires ou d'échantillons microscopiques."

    def apply(self, image: cv2.Mat, params: Dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(image, markers)
        image[markers == -1] = [0, 0, 255]  # contours en rouge

        return image