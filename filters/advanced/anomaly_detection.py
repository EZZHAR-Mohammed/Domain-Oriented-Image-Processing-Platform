# filters/advanced/anomaly_detection.py
import cv2
import numpy as np
from filters.base_filter import BaseFilter


class AnomalyDetection(BaseFilter):
    def __init__(self):
        super().__init__()
        self.name = "Détection d'anomalies (variance locale)"
        self.category = "Avancé / Détection"
        self.description = "Met en évidence les zones anormales via écart-type local"

    def apply(self, image, params):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mean, stddev = cv2.meanStdDev(gray)
        threshold = params.get("threshold", 3.0) * stddev[0][0]
        anomalies = cv2.absdiff(gray, mean[0][0]) > threshold
        anomalies = anomalies.astype(np.uint8) * 255
        # Coloration rouge des anomalies
        result = image.copy()
        result[anomalies == 255] = [0, 0, 255]
        return result

    def get_default_params(self):
        return {"threshold": 3.0}