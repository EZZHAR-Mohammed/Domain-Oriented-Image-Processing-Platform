# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QSplitter, QAction, QComboBox, QLabel
from PyQt5.QtCore import Qt
import cv2
import numpy as np

from ui.image_viewer import ImageViewer
from ui.filter_panel import FilterPanel
from ui.toolbar import AppToolBar

from core.image_manager import ImageManager
from core.history_manager import HistoryManager
from core.domain_manager import DomainManager
from core.filter_manager import FilterManager
from core.recommendation_engine import RecommendationEngine

from utils.report_generator import generate_pdf_report


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Traitement d'images par domaine")
        self.resize(1400, 900)

        # Managers
        self.image_manager = ImageManager()
        self.history_manager = HistoryManager()
        self.domain_manager = DomainManager()
        self.filter_manager = FilterManager(self.image_manager, self.history_manager)
        self.rec_engine = RecommendationEngine()

        self.current_filters = []

        # UI centrale
        self.viewer = ImageViewer(self)
        self.filter_panel = FilterPanel(self.filter_manager, self, self)  # main_window passé explicitement

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.viewer)
        splitter.addWidget(self.filter_panel)
        splitter.setSizes([900, 500])
        self.setCentralWidget(splitter)

        # Toolbar
        self.toolbar = AppToolBar(self)
        self.addToolBar(self.toolbar)

        # Connexions toolbar
        self.toolbar.undoRequested.connect(self.on_undo)
        self.toolbar.redoRequested.connect(self.on_redo)
        self.toolbar.resetRequested.connect(self.on_reset)
        self.toolbar.rotateRequested.connect(self.on_rotate)
        self.toolbar.compareRequested.connect(self.on_compare)
        self.toolbar.recommendRequested.connect(self.on_recommend)
        self.toolbar.zoom_in_requested.connect(self.on_zoom_in)
        self.toolbar.zoom_out_requested.connect(self.on_zoom_out)

        # Menu Fichier
        file_menu = self.menuBar().addMenu("Fichier")
        open_act = QAction("Ouvrir image...", self)
        open_act.triggered.connect(self.open_image)
        file_menu.addAction(open_act)

        save_act = QAction("Enregistrer sous...", self)
        save_act.triggered.connect(self.save_image)
        file_menu.addAction(save_act)

        export_act = QAction("Exporter rapport PDF", self)
        export_act.triggered.connect(self.export_report)
        file_menu.addAction(export_act)

        # ───────────────────────────────────────────────
        # Nouveau : ComboBox pour choisir le domaine
        # ───────────────────────────────────────────────
        self.domain_combo = QComboBox()
        domains = self.domain_manager.get_domain_names()  # ["Général", "Santé", ...]
        self.domain_combo.addItems(domains)
        self.domain_combo.currentTextChanged.connect(self.on_domain_selected)

        # Ajout dans la toolbar (à gauche ou à droite selon préférence)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(QLabel("Domaine : "))
        self.toolbar.addWidget(self.domain_combo)

        # Démarrage automatique sur "Général" (ou premier domaine)
        default_domain = "Général" if "Général" in domains else domains[0]
        self.domain_combo.setCurrentText(default_domain)
        self.on_domain_selected(default_domain)  # Charge les filtres dès le démarrage

        # Plus besoin de self.domain_dialog.exec_() → l'app s'ouvre directement

    def on_domain_selected(self, domain_name: str):
        success = self.domain_manager.set_domain(domain_name)
        if success:
            self.current_filters = self.domain_manager.get_current_filters()
            self.filter_panel.load_filters(self.current_filters)
            self.setWindowTitle(f"Traitement d'images – {domain_name}")
            print(f"Domaine changé : {domain_name}")
        else:
            QMessageBox.warning(self, "Erreur", f"Domaine '{domain_name}' non reconnu")

    def open_image(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Ouvrir une image",
            "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)")
        if path:
            if self.image_manager.load_image(path):
                self.viewer.display_image(self.image_manager.get_current())
                self.history_manager.save_state(self.image_manager.get_current())
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de lire l'image")

    def save_image(self):
        if self.image_manager.get_current() is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer l'image",
            "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;TIFF (*.tif *.tiff)")
        if path:
            if self.image_manager.save_current(path):
                QMessageBox.information(self, "Succès", "Image enregistrée")
            else:
                QMessageBox.warning(self, "Erreur", "Échec de l'enregistrement")

    def export_report(self):
        if self.image_manager.get_original() is None:
            QMessageBox.warning(self, "Erreur", "Aucune image chargée")
            return

        path, _ = QFileDialog.getSaveFileName(
            self, "Exporter rapport PDF", "", "PDF (*.pdf)")
        if path:
            domain = self.domain_manager.get_current_domain_name() or "Général"
            generate_pdf_report(
                self.image_manager.get_original(),
                self.image_manager.get_current(),
                path,
                domain=domain
            )
            QMessageBox.information(self, "Succès", "Rapport PDF créé")

    def on_undo(self):
        if self.history_manager.can_undo():
            img = self.history_manager.undo()
            if img is not None:
                self.image_manager.set_current(img)
                self.viewer.display_image(img)

    def on_redo(self):
        if self.history_manager.can_redo():
            img = self.history_manager.redo()
            if img is not None:
                self.image_manager.set_current(img)
                self.viewer.display_image(img)

    def on_reset(self):
        self.image_manager.reset_to_original()
        img = self.image_manager.get_current()
        self.viewer.display_image(img)
        self.history_manager.save_state(img)

    def on_rotate(self):
        img = self.image_manager.get_current()
        if img is not None:
            rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            self.image_manager.set_current(rotated)
            self.viewer.display_image(rotated)
            self.history_manager.save_state(rotated)

    def on_compare(self):
        orig = self.image_manager.get_original()
        curr = self.image_manager.get_current()
        if orig is None or curr is None:
            return

        h_orig, w_orig = orig.shape[:2]
        h_curr, w_curr = curr.shape[:2]
        h = max(h_orig, h_curr)
        combined = np.zeros((h, w_orig + w_curr, 3), dtype=np.uint8)
        combined[:h_orig, :w_orig] = orig
        combined[:h_curr, w_orig:w_orig + w_curr] = curr
        self.viewer.display_image(combined)

    def on_recommend(self):
        curr_img = self.image_manager.get_current()
        if curr_img is None:
            return

        analysis = self.rec_engine.analyze_image(curr_img)
        domain = self.domain_manager.get_current_domain_name()
        suggestions = self.rec_engine.suggest_filters(analysis, domain)

        if suggestions:
            msg = "Suggestions de filtres :\n• " + "\n• ".join(suggestions)
        else:
            msg = "Aucune suggestion particulière pour cette image."

        QMessageBox.information(self, "Recommandations", msg)

    # ───────────────────────────────────────────────
    # Nouvelles méthodes pour zoom
    # ───────────────────────────────────────────────
    def on_zoom_in(self):
        self.viewer.zoom(1.25)   # Zoom +25%

    def on_zoom_out(self):
        self.viewer.zoom(0.8)    # Zoom -20%