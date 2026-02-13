# filters/biology/cell_counting.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class CellCounting(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Comptage de cellules"
        self.category = "Biologie / Analyse"
        self.description = "Compte le nombre de cellules ou d'objets dans une image biologique en utilisant la détection de contours. Utile pour l'analyse de cultures cellulaires ou d'échantillons microscopiques."
    def apply(self, image: cv2.Mat, params: dict) -> cv2.Mat:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        result = image.copy()
        cv2.drawContours(result, contours, -1, (0,255,0), 2)
        count = len(contours)
        cv2.putText(result, f"Cellules : {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
        return result