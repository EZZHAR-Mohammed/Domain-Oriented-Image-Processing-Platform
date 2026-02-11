# ui/toolbar.py
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import pyqtSignal


class AppToolBar(QToolBar):
    undoRequested = pyqtSignal()
    redoRequested = pyqtSignal()
    resetRequested = pyqtSignal()
    rotateRequested = pyqtSignal()
    compareRequested = pyqtSignal()
    recommendRequested = pyqtSignal()
    zoom_in_requested = pyqtSignal()   # Nouveau
    zoom_out_requested = pyqtSignal()  # Nouveau

    def __init__(self, parent=None):
        super().__init__("Outils", parent)

        # Undo / Redo
        self.addAction("Undo", self.undoRequested.emit)
        self.addAction("Redo", self.redoRequested.emit)

        self.addSeparator()

        # Reset / Rotate
        self.addAction("Reset", self.resetRequested.emit)
        self.addAction("Rotate 90°", self.rotateRequested.emit)

        self.addSeparator()

        # Comparer / Recommandations
        self.addAction("Comparer avant/après", self.compareRequested.emit)
        self.addAction("Recommandations", self.recommendRequested.emit)

        self.addSeparator()

        # ───────────────────────────────
        # Boutons Zoom In / Zoom Out
        # ───────────────────────────────
        zoom_in_act = QAction("Zoom In (+)", self)
        zoom_in_act.triggered.connect(self.zoom_in_requested.emit)
        self.addAction(zoom_in_act)

        zoom_out_act = QAction("Zoom Out (-)", self)
        zoom_out_act.triggered.connect(self.zoom_out_requested.emit)
        self.addAction(zoom_out_act)