# ui/image_viewer.py
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QImage, QTransform
from PyQt5.QtCore import Qt
import cv2


class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)

        # Configuration pour le drag (pan) et le zoom avec molette
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        # Utiliser le centre de la vue comme ancre de transformation
        # afin que les zooms restent centrés sur la vue
        self.setTransformationAnchor(QGraphicsView.AnchorViewCenter)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        # Variables pour conserver le zoom et l'état
        self.zoom_factor = 1.0
        self.has_been_displayed = False  # Pour savoir si c'est la première fois qu'on affiche une image

    def display_image(self, cv_img):
        """
        Affiche ou met à jour l'image sans réinitialiser le zoom
        (sauf la toute première fois où on fait un fitInView)
        """
        if cv_img is None:
            self.pixmap_item.setPixmap(QPixmap())
            self.has_been_displayed = False
            return

        # Conversion OpenCV (BGR) → QImage (RGB)
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_img = q_img.rgbSwapped()  # BGR → RGB

        pixmap = QPixmap.fromImage(q_img)
        self.pixmap_item.setPixmap(pixmap)

        # Première fois qu'on charge une image → on ajuste à la vue
        # et on réduit légèrement pour laisser une marge (image
        # un peu plus petite que la vue). Après cela on conserve
        # le zoom actuel mais on recentre toujours l'image quand
        # elle est mise à jour (ex: après application d'un filtre).
        if not self.has_been_displayed:
            self.resetTransform()
            self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
            # Légère réduction pour que l'image soit un peu plus petite
            margin_scale = 0.95
            self.scale(margin_scale, margin_scale)
            self.zoom_factor = margin_scale
            self.has_been_displayed = True
            self.centerOn(self.pixmap_item)
        else:
            # Conserver le zoom mais recentrer l'image
            if self.pixmap_item.pixmap():
                self.centerOn(self.pixmap_item)

    def zoom(self, factor: float):
        """Applique un zoom relatif (ex: 1.25 pour zoom in, 0.8 pour zoom out)"""
        self.zoom_factor *= factor
        self.scale(factor, factor)
        # Recentrer après zoom pour garder l'image au centre
        if self.pixmap_item.pixmap():
            self.centerOn(self.pixmap_item)

    def reset_zoom(self):
        """Remet le zoom à 1.0 et ajuste à la vue"""
        self.resetTransform()
        self.zoom_factor = 1.0
        self.has_been_displayed = False  # pour forcer un nouveau fitInView
        if self.pixmap_item.pixmap():
            self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
            # appliquer la même marge que pour l'affichage initial
            margin_scale = 0.95
            self.scale(margin_scale, margin_scale)
            self.zoom_factor = margin_scale
            self.has_been_displayed = True
            self.centerOn(self.pixmap_item)

    def rotate90(self):
        """Rotation de 90° sans perdre le zoom"""
        transform = QTransform().rotate(90)
        self.pixmap_item.setTransform(transform, combineWithParent=True)
        # Pas besoin de refaire fitInView → le zoom est conservé
        # Recentrer après rotation
        if self.pixmap_item.pixmap():
            self.centerOn(self.pixmap_item)