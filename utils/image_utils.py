# utils/image_utils.py
import cv2
import numpy as np


def to_grayscale(img):
    """Convertit en niveaux de gris si ce n'est pas déjà le cas"""
    if len(img.shape) == 3 and img.shape[2] == 3:
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def normalize_8bit(img):
    """Ramène une image en uint8 [0-255]"""
    if img.dtype != np.uint8:
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
        img = img.astype(np.uint8)
    return img


def resize_keep_aspect(img, max_size=1200):
    """Redimensionne en conservant le ratio, sans dépasser max_size"""
    h, w = img.shape[:2]
    if max(h, w) <= max_size:
        return img

    ratio = max_size / max(h, w)
    new_size = (int(w * ratio), int(h * ratio))
    return cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)


def get_image_info(img):
    """Retourne un dictionnaire d'informations basiques sur l'image"""
    if img is None:
        return {"valid": False}

    h, w = img.shape[:2]
    channels = img.shape[2] if len(img.shape) == 3 else 1
    dtype = str(img.dtype)

    return {
        "valid": True,
        "width": w,
        "height": h,
        "channels": channels,
        "dtype": dtype,
        "size_bytes": img.nbytes
    }