import cv2
import numpy as np

class RecommendationEngine:
    @staticmethod
    def analyze_image(img):
        if img is None:
            return {}

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])

        mean = np.mean(gray)
        std = np.std(gray)
        entropy = -np.sum((hist / hist.sum()) * np.log2(hist / hist.sum() + 1e-10))

        return {
            "mean_brightness": float(mean),
            "contrast": float(std),
            "entropy": float(entropy),
            "size": img.shape[:2]
        }

    @staticmethod
    def suggest_filters(analysis, domain_name):
        suggestions = []

        if analysis.get("contrast", 0) < 40:
            suggestions.append("Amélioration de contraste")

        if analysis.get("entropy", 0) < 6.0:
            suggestions.append("Réduction de bruit / lissage")

        if domain_name == "Santé":
            suggestions.append("Égalisation d'histogramme")
            suggestions.append("Amélioration osseuse")
        elif domain_name == "Militaire":
            suggestions.append("Détection de contours (Canny)")
        elif domain_name == "Biologie":
            suggestions.append("Segmentation cellulaire")
        elif domain_name == "Satellite":
            suggestions.append("Indice de végétation")

        return suggestions[:4]  # on limite à 4 suggestions