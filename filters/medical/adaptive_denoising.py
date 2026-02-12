# filters/medical/adaptive_denoising.py
import cv2
from filters.base_filter import BaseFilter


class AdaptiveDenoising(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Débruitage adaptatif NLM"
        self.category = "Médical / Débruitage"
        self.description = "Réduction de bruit non-local means – très efficace pour IRM/radiographie"

    def apply(self, image, params):
        h = params.get("h", 10)
        hColor = params.get("hColor", 10)
        templateWindowSize = params.get("template", 7)
        searchWindowSize = params.get("search", 21)
        return cv2.fastNlMeansDenoisingColored(
            image, None, h, hColor, templateWindowSize, searchWindowSize
        )

    def get_default_params(self):
        return {"h": 10, "hColor": 10, "template": 7, "search": 21}