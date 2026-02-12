# ui/toolbar.py
from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon


class AppToolBar(QToolBar):
    undoRequested = pyqtSignal()
    redoRequested = pyqtSignal()
    resetRequested = pyqtSignal()
    rotateRequested = pyqtSignal()
    compareRequested = pyqtSignal()
    recommendRequested = pyqtSignal()
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Outils", parent)

        # Undo
        undo_act = QAction(QIcon("assets/icons/icons8-undo-48.png"), "", self)
        undo_act.setToolTip("Annuler (Undo)")
        undo_act.triggered.connect(self.undoRequested.emit)
        self.addAction(undo_act)

        # Redo
        redo_act = QAction(QIcon("assets/icons/icons8-redo-48.png"), "", self)
        redo_act.setToolTip("Rétablir (Redo)")
        redo_act.triggered.connect(self.redoRequested.emit)
        self.addAction(redo_act)

        self.addSeparator()

        # Reset
        reset_act = QAction(QIcon("assets/icons/icons8-refresh-48.png"), "", self)
        reset_act.setToolTip("Réinitialiser l'image")
        reset_act.triggered.connect(self.resetRequested.emit)
        self.addAction(reset_act)

        # Rotate
        rotate_act = QAction(QIcon("assets/icons/icons8-rotate-48.png"), "", self)
        rotate_act.setToolTip("Rotation 90°")
        rotate_act.triggered.connect(self.rotateRequested.emit)
        self.addAction(rotate_act)

        self.addSeparator()

        # Comparer avant/après
        compare_act = QAction(QIcon("assets/icons/icons8-space-before-paragraph-48.png"), "", self)
        compare_act.setToolTip("Comparer avant / après")
        compare_act.triggered.connect(self.compareRequested.emit)
        self.addAction(compare_act)

        # Recommandations
        recommend_act = QAction(QIcon("assets/icons/icons8-idea-40.png"), "", self)
        recommend_act.setToolTip("Recommandations de filtres")
        recommend_act.triggered.connect(self.recommendRequested.emit)
        self.addAction(recommend_act)

        self.addSeparator()

        # Zoom In
        zoom_in_act = QAction(QIcon("assets/icons/icons8-zoom-in-48.png"), "", self)
        zoom_in_act.setToolTip("Zoom avant (+)")
        zoom_in_act.triggered.connect(self.zoom_in_requested.emit)
        self.addAction(zoom_in_act)

        # Zoom Out
        zoom_out_act = QAction(QIcon("assets/icons/icons8-zoom-out-48.png"), "", self)
        zoom_out_act.setToolTip("Zoom arrière (-)")
        zoom_out_act.triggered.connect(self.zoom_out_requested.emit)
        self.addAction(zoom_out_act)


