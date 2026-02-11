# utils/file_io.py
import cv2
import os
from PyQt5.QtWidgets import QFileDialog


def open_image_dialog(parent=None, title="Ouvrir une image"):
    """Ouvre une boîte de dialogue pour sélectionner une image"""
    filters = "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
    path, _ = QFileDialog.getOpenFileName(parent, title, "", filters)
    return path if path and os.path.isfile(path) else None


def save_image_dialog(parent=None, title="Enregistrer l'image", default_name="image_traitee"):
    """Ouvre une boîte de dialogue pour choisir où sauvegarder l'image"""
    filters = "PNG (*.png);;JPEG (*.jpg *.jpeg);;BMP (*.bmp);;TIFF (*.tif *.tiff)"
    path, selected_filter = QFileDialog.getSaveFileName(
        parent, title,
        default_name,
        filters
    )
    if not path:
        return None

    # Ajouter l'extension si absente
    if '.' not in os.path.basename(path):
        ext = selected_filter.split("(*")[1].split(")")[0].strip("*")
        path += ext

    return path


def save_image_cv(img, path):
    """Sauvegarde une image OpenCV sans message d'erreur verbeux"""
    if img is None:
        return False
    try:
        success = cv2.imwrite(path, img)
        return success
    except Exception:
        return False