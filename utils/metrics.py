# utils/metrics.py
import cv2
import numpy as np


def psnr(original, processed):
    """Calcule le PSNR entre deux images (plus c'est élevé, mieux c'est)"""
    if original.shape != processed.shape:
        return float('nan')
    return cv2.PSNR(original, processed)


def mse(original, processed):
    """Mean Squared Error"""
    if original.shape != processed.shape:
        return float('nan')
    err = original.astype(float) - processed.astype(float)
    return np.mean(err ** 2)


def ssim(original, processed):
    """
    SSIM simplifié (OpenCV a une implémentation, mais on peut utiliser skimage aussi)
    Retourne une valeur entre -1 et 1 (1 = identique)
    """
    try:
        from skimage.metrics import structural_similarity
        if len(original.shape) == 3:
            original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)
        return structural_similarity(original, processed, data_range=255)
    except ImportError:
        # Fallback très basique si skimage n'est pas installé
        return float('nan')


def compute_all_metrics(original, processed):
    """Retourne un dictionnaire avec plusieurs métriques"""
    if original is None or processed is None:
        return {"error": "Images manquantes"}

    return {
        "PSNR": psnr(original, processed),
        "MSE": mse(original, processed),
        "SSIM": ssim(original, processed),
    }