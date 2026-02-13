# filters/general/edge_sharpening.py
import cv2
from filters.base_filter import BaseFilter


class EdgeSharpening(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Netteté des bords (Unsharp Mask)"
        self.category = "Général / Enhancement"
        self.description = "Améliore la netteté des bords en utilisant la technique de l'Unsharp Mask. Idéal pour renforcer les détails et les contours dans une image."

    def apply(self, image: cv2.Mat, params: dict) -> cv2.Mat:
        sigma = params.get("sigma", 1.0)
        amount = params.get("amount", 1.5)
        threshold = params.get("threshold", 0)
        blurred = cv2.GaussianBlur(image, (0,0), sigma)
        sharpened = cv2.addWeighted(image, 1.0 + amount, blurred, -amount, 0)
        return sharpened

    def get_default_params(self) -> dict:
        return {"sigma": 1.0, "amount": 1.5, "threshold": 0}