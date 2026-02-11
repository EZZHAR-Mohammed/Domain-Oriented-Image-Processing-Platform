from PyQt5.QtWidgets import QToolBar, QAction
from PyQt5.QtCore import pyqtSignal

class AppToolBar(QToolBar):
    undoRequested = pyqtSignal()
    redoRequested = pyqtSignal()
    resetRequested = pyqtSignal()
    rotateRequested = pyqtSignal()
    compareRequested = pyqtSignal()
    recommendRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__("Outils", parent)

        self.addAction("Undo", self.undoRequested.emit)
        self.addAction("Redo", self.redoRequested.emit)
        self.addSeparator()
        self.addAction("Reset", self.resetRequested.emit)
        self.addAction("Rotate 90°", self.rotateRequested.emit)
        self.addSeparator()
        self.addAction("Comparer avant/après", self.compareRequested.emit)
        self.addAction("Recommandations", self.recommendRequested.emit)