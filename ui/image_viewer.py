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

        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self.zoom_factor = 1.0

    def display_image(self, cv_img):
        if cv_img is None:
            self.pixmap_item.setPixmap(QPixmap())
            return

        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        q_img = QImage(cv_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
        q_img = q_img.rgbSwapped()  # OpenCV est BGR → on convertit

        pixmap = QPixmap.fromImage(q_img)
        self.pixmap_item.setPixmap(pixmap)

        self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def zoom(self, factor):
        self.zoom_factor *= factor
        self.scale(factor, factor)

    def reset_zoom(self):
        self.resetTransform()
        self.zoom_factor = 1.0
        self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)

    def rotate90(self):
        transform = QTransform().rotate(90)
        self.pixmap_item.setTransform(transform, combineWithParent=True)