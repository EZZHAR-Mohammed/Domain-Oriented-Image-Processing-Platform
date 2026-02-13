# ui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QSplitter, QAction, QComboBox, QLabel, QDialog, QVBoxLayout, QListWidget, QPushButton
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import os

from ui.image_viewer import ImageViewer
from ui.filter_panel import FilterPanel
from ui.toolbar import AppToolBar
from ui.filter_params_dialog import FilterParamsDialog  # Pour sliders

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

        # Support multi-images
        self.loaded_images = []           # Liste de np.ndarray
        self.image_filenames = []         # Noms pour affichage
        self.current_image_index = -1

        # Suivi filtres pour PDF
        self.applied_filters = []

        # UI
        self.viewer = ImageViewer(self)
        self.filter_panel = FilterPanel(self.filter_manager, self, self)

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
        open_act = QAction("Ouvrir image(s)...", self)
        open_act.triggered.connect(self.open_image)
        file_menu.addAction(open_act)

        save_act = QAction("Enregistrer l'image actuelle", self)
        save_act.triggered.connect(self.save_image)
        file_menu.addAction(save_act)

        # ───────────────────────────────────────────────
        # Nouveau : Enregistrer toutes les images traitées
        # ───────────────────────────────────────────────
        save_all_act = QAction("Enregistrer toutes les images traitées", self)
        save_all_act.triggered.connect(self.on_save_all_processed)
        file_menu.addAction(save_all_act)

        export_act = QAction("Exporter rapport PDF", self)
        export_act.triggered.connect(self.export_report)
        file_menu.addAction(export_act)

        # Menu Batch
        batch_menu = self.menuBar().addMenu("Batch")
        batch_act = QAction("Appliquer plusieurs filtres à toutes les images", self)
        batch_act.triggered.connect(self.on_batch_process)
        batch_menu.addAction(batch_act)

        # Sélecteur d'images
        self.image_selector = QComboBox()
        self.image_selector.currentIndexChanged.connect(self.on_image_selected)
        self.toolbar.addSeparator()
        self.toolbar.addWidget(QLabel("Image : "))
        self.toolbar.addWidget(self.image_selector)

        # Combo domaine
        self.domain_combo = QComboBox()
        domains = self.domain_manager.get_domain_names()
        self.domain_combo.addItems(domains)
        self.domain_combo.currentTextChanged.connect(self.on_domain_selected)

        self.toolbar.addSeparator()
        self.toolbar.addWidget(QLabel("Domaine : "))
        self.toolbar.addWidget(self.domain_combo)

        default_domain = "Général" if "Général" in domains else domains[0]
        self.domain_combo.setCurrentText(default_domain)
        self.on_domain_selected(default_domain)

    def on_domain_selected(self, domain_name: str):
        success = self.domain_manager.set_domain(domain_name)
        if success:
            self.current_filters = self.domain_manager.get_current_filters()
            self.filter_panel.load_filters(self.current_filters)
            self.setWindowTitle(f"Traitement d'images – {domain_name}")
            print(f"Domaine changé : {domain_name}")
        else:
            QMessageBox.warning(self, "Erreur", f"Domaine '{domain_name}' non reconnu")

    def on_image_selected(self, index):
        if 0 <= index < len(self.loaded_images):
            self.current_image_index = index
            self.image_manager.current_image = self.loaded_images[index].copy()
            self.viewer.display_image(self.image_manager.get_current())
            self.history_manager.save_state(self.image_manager.get_current())

    def open_image(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Ouvrir une ou plusieurs images",
            "", "Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)")
        if not paths:
            return

        self.loaded_images = []
        self.image_filenames = []
        self.image_selector.clear()
        self.current_image_index = -1

        for path in paths:
            if self.image_manager.load_image(path):
                img_copy = self.image_manager.get_current().copy()
                self.loaded_images.append(img_copy)
                filename = os.path.basename(path)
                self.image_filenames.append(filename)
                self.image_selector.addItem(filename)
            else:
                QMessageBox.warning(self, "Erreur", f"Impossible de lire {path}")

        if self.loaded_images:
            self.current_image_index = 0
            self.image_manager.current_image = self.loaded_images[0].copy()
            self.viewer.display_image(self.image_manager.get_current())
            self.history_manager.save_state(self.image_manager.get_current())
            QMessageBox.information(self, "Succès", f"{len(self.loaded_images)} image(s) chargée(s)")

    def save_image(self):
        if self.image_manager.get_current() is None:
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Enregistrer l'image actuelle",
            "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;TIFF (*.tif *.tiff)")
        if path:
            if self.image_manager.save_current(path):
                QMessageBox.information(self, "Succès", "Image enregistrée")
            else:
                QMessageBox.warning(self, "Erreur", "Échec de l'enregistrement")

    def on_save_all_processed(self):
        if not self.loaded_images:
            QMessageBox.warning(self, "Erreur", "Aucune image chargée à enregistrer")
            return

        # Choisir un dossier
        output_dir = QFileDialog.getExistingDirectory(self, "Choisir dossier pour enregistrer toutes les images traitées")
        if not output_dir:
            return

        saved_count = 0
        for i, img in enumerate(self.loaded_images):
            if img is None:
                continue

            base_name = self.image_filenames[i] if i < len(self.image_filenames) else f"image_{i+1}"
            base_name = os.path.splitext(base_name)[0]  # Sans extension

            output_path = os.path.join(output_dir, f"{base_name}_processed.png")
            if cv2.imwrite(output_path, img):
                saved_count += 1
            else:
                print(f"Échec enregistrement : {output_path}")

        QMessageBox.information(self, "Succès", f"{saved_count} images enregistrées dans {output_dir}")

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
                domain=domain,
                applied_filters=self.applied_filters
            )
            QMessageBox.information(self, "Succès", "Rapport PDF créé")

    def on_batch_process(self):
        if not self.loaded_images:
            QMessageBox.warning(self, "Erreur", "Chargez d'abord plusieurs images")
            return

        # Dialogue choix séquence de filtres
        dialog = QDialog(self)
        dialog.setWindowTitle("Batch : Choisir filtres (appliqués à toutes les images)")
        layout = QVBoxLayout(dialog)

        layout.addWidget(QLabel(f"Appliquer une séquence sur {len(self.loaded_images)} image(s)"))

        filter_list = QListWidget()
        filter_list.setSelectionMode(QListWidget.MultiSelection)
        for filt in self.current_filters:
            filter_list.addItem(f"{filt.name} ({filt.category})")
        layout.addWidget(filter_list)

        apply_btn = QPushButton("Voir/Appliquer la séquence")
        apply_btn.clicked.connect(dialog.accept)
        layout.addWidget(apply_btn)

        if dialog.exec_() == QDialog.Accepted:
            selected_items = filter_list.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, "Erreur", "Sélectionnez au moins un filtre")
                return

            # Récupère les filtres dans l'ordre choisi
            selected_filters = []
            for item in selected_items:
                row = filter_list.row(item)
                selected_filters.append(self.current_filters[row])

            # Pour chaque filtre : demander params une fois (preview live)
            sequence_params = []
            for filt in selected_filters:
                params = filt.get_default_params()
                if params:
                    param_dialog = FilterParamsDialog(filt, self, self)
                    param_dialog.previewRequested.connect(lambda p: self.preview_filter(filt, p))
                    if param_dialog.exec_() != QDialog.Accepted:
                        QMessageBox.information(self, "Info", "Batch annulé")
                        return
                    params = param_dialog.get_params()
                sequence_params.append(params)

            # Confirmation finale
            reply = QMessageBox.question(
                self, "Confirmer batch massif",
                f"Appliquer {len(selected_filters)} filtres à {len(self.loaded_images)} images ?\n"
                f"Les modifications seront visibles sur l'image sélectionnée en temps réel.",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply != QMessageBox.Yes:
                return

            # Application séquentielle sur TOUTES les images
            for i in range(len(self.loaded_images)):
                current = self.loaded_images[i].copy()
                for j, filt in enumerate(selected_filters):
                    current = filt.apply(current, sequence_params[j])
                self.loaded_images[i] = current  # Mise à jour

            # Rafraîchissement de l'image affichée
            if self.current_image_index >= 0:
                self.image_manager.current_image = self.loaded_images[self.current_image_index].copy()
                self.viewer.display_image(self.image_manager.get_current())
                self.history_manager.save_state(self.image_manager.get_current())

            QMessageBox.information(self, "Succès", f"Toutes les images ont été traitées avec la séquence")

    def preview_filter(self, filter_instance, params):
        current_img = self.image_manager.get_current()
        if current_img is None:
            return
        try:
            preview_img = filter_instance.apply(current_img.copy(), params)
            if preview_img is not None:
                self.viewer.display_image(preview_img)
        except Exception as e:
            print(f"Erreur preview batch : {e}")

    def on_undo(self):
        if self.history_manager.can_undo():
            img = self.history_manager.undo()
            if img is not None:
                self.image_manager.set_current(img)
                self.viewer.display_image(img)

                # Mise à jour dans la liste multi-images (pour reset correct)
                if self.current_image_index >= 0:
                    self.loaded_images[self.current_image_index] = img.copy()

    def on_redo(self):
        if self.history_manager.can_redo():
            img = self.history_manager.redo()
            if img is not None:
                self.image_manager.set_current(img)
                self.viewer.display_image(img)

                # Mise à jour dans la liste multi-images
                if self.current_image_index >= 0:
                    self.loaded_images[self.current_image_index] = img.copy()

    def on_reset(self):
        self.image_manager.reset_to_original()
        img = self.image_manager.get_current()
        self.viewer.display_image(img)
        self.history_manager.save_state(img)

        # Mise à jour dans la liste multi-images (pour reset correct sur toutes)
        if self.current_image_index >= 0:
            self.loaded_images[self.current_image_index] = img.copy()

    def on_rotate(self):
        img = self.image_manager.get_current()
        if img is not None:
            rotated = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            self.image_manager.set_current(rotated)
            self.viewer.display_image(rotated)
            self.history_manager.save_state(rotated)

            # Mise à jour dans la liste multi-images
            if self.current_image_index >= 0:
                self.loaded_images[self.current_image_index] = rotated.copy()

    # Les autres méthodes (on_compare, on_recommend, on_zoom_in, on_zoom_out) restent inchangées
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

    def on_zoom_in(self):
        self.viewer.zoom(1.25)

    def on_zoom_out(self):
        self.viewer.zoom(0.8)