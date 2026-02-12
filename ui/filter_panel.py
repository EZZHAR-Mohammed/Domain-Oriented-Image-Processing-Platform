# ui/filter_panel.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QDialog
)
from PyQt5.QtCore import Qt

from ui.filter_params_dialog import FilterParamsDialog


class FilterPanel(QWidget):
    def __init__(self, filter_manager, main_window, parent=None):
        super().__init__(parent)
        self.filter_manager = filter_manager
        self.main_window = main_window

        self.setMinimumWidth(280)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(QLabel("Filtres disponibles"))

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content = QWidget()
        self.filters_layout = QVBoxLayout(self.content)
        self.filters_layout.setAlignment(Qt.AlignTop)
        self.scroll.setWidget(self.content)

        main_layout.addWidget(self.scroll)

    def clear_filters(self):
        while self.filters_layout.count():
            item = self.filters_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_filters(self, filters_list):
        self.clear_filters()
        for filt in filters_list:
            btn = QPushButton(filt.name)
            btn.setToolTip(filt.description if hasattr(filt, 'description') else "")
            btn.clicked.connect(lambda checked, f=filt: self.apply_filter(f))
            self.filters_layout.addWidget(btn)

    def apply_filter(self, filter_instance):
        if self.filter_manager is None:
            print("Erreur : filter_manager non disponible")
            return

        params = filter_instance.get_default_params()

        # Si le filtre a des paramètres → ouvrir dialogue avec preview live
        if params:
            dialog = FilterParamsDialog(filter_instance, self.main_window, self)
            # Connexion preview live
            dialog.previewRequested.connect(lambda p: self.preview_filter(filter_instance, p))
            if dialog.exec_() == QDialog.Accepted:
                params = dialog.get_params()
            else:
                return  # Annulé
        else:
            # Pas de params → applique direct
            pass

        success = self.filter_manager.apply_filter(filter_instance, params)

        if success:
            # Ajout au suivi pour export PDF
            if hasattr(self.main_window, 'applied_filters'):
                self.main_window.applied_filters.append((filter_instance.name, params.copy()))

            # Rafraîchissement final
            img = self.main_window.image_manager.get_current()
            if img is not None:
                self.main_window.viewer.display_image(img)
                print(f"Filtre appliqué définitivement : {filter_instance.name}")
        else:
            print(f"Échec application filtre : {filter_instance.name}")

    def preview_filter(self, filter_instance, params):
        """Prévisualisation live sans toucher à l'historique"""
        current_img = self.main_window.image_manager.get_current()
        if current_img is None:
            return

        try:
            preview_img = filter_instance.apply(current_img.copy(), params)
            if preview_img is not None:
                self.main_window.viewer.display_image(preview_img)
        except Exception as e:
            print(f"Erreur pendant preview : {e}")