# ui/filter_panel.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt

class FilterPanel(QWidget):
    def __init__(self, filter_manager, parent=None):
        super().__init__(parent)
        self.filter_manager = filter_manager  # Important : on garde la référence

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
            # Connexion corrigée
            btn.clicked.connect(lambda checked, f=filt: self.apply_filter(f))
            self.filters_layout.addWidget(btn)

    def apply_filter(self, filter_instance):
        """Méthode qui manquait → c'est elle qui corrige l'erreur"""
        if self.filter_manager is None:
            print("Erreur : filter_manager non disponible")
            return

        # Pour l'instant : params par défaut
        # (plus tard : ouvrir un dialogue pour sliders)
        params = filter_instance.get_default_params()

        success = self.filter_manager.apply_filter(filter_instance, params)

        if success:
            # Rafraîchir l'affichage de l'image
            if hasattr(self.parent(), 'image_viewer') and hasattr(self.parent(), 'image_manager'):
                img = self.parent().image_manager.get_image()  # ou .get_current()
                if img is not None:
                    self.parent().image_viewer.display_image(img)
            print(f"Filtre appliqué : {filter_instance.name}")
        else:
            print(f"Échec application filtre : {filter_instance.name}")