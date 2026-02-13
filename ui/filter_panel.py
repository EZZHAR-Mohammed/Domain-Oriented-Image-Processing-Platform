# ui/filter_panel.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea, QDialog,
    QFrame, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt

from ui.filter_params_dialog import FilterParamsDialog


class FilterPanel(QWidget):
    def __init__(self, filter_manager, main_window, parent=None):
        super().__init__(parent)
        self.filter_manager = filter_manager
        self.main_window = main_window

        self.setMinimumWidth(340)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(10)

        # Titre propre
        title_label = QLabel("Filtres disponibles")
        title_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addSpacing(12)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.NoFrame)
        self.content = QWidget()
        self.filters_layout = QVBoxLayout(self.content)
        self.filters_layout.setAlignment(Qt.AlignTop)
        self.filters_layout.setSpacing(18)
        self.filters_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll.setWidget(self.content)

        main_layout.addWidget(self.scroll)

        # Scrollbar discrète
        self.scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: transparent;
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(100, 100, 100, 0.4);
                min-height: 30px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

    def clear_filters(self):
        while self.filters_layout.count():
            item = self.filters_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_filters(self, filters_list):
        self.clear_filters()

        for filt in filters_list:
            # Carte stylée
            card = QFrame(self.content)
            card.setFrameShape(QFrame.StyledPanel)
            card.setFrameShadow(QFrame.Raised)
            card.setFixedHeight(130)  # Hauteur fixe pour forcer 3 lignes visibles minimum
            card.setStyleSheet("""
                QFrame {
                    background-color: #ffffff;
                    border: 1px solid #d0d7e0;
                    border-radius: 12px;
                    margin: 8px 4px;
                }
                QFrame:hover {
                    background-color: #f0f7ff;
                    border: 1px solid #3b82f6;
                    box-shadow: none;
                }
            """)

            card_layout = QHBoxLayout(card)
            card_layout.setContentsMargins(16, 12, 16, 12)
            card_layout.setSpacing(18)

            # Icône à gauche
            icon_label = QLabel()
            icon_name = filt.name.lower().replace(" ", "_").replace("–", "").replace("(", "").replace(")", "").replace("é", "e").replace("è", "e")
            icon_path = f"assets/icons/icons8-{icon_name}-48.png"

            if os.path.exists(icon_path):
                pixmap = QIcon(icon_path).pixmap(64, 64)
                icon_label.setPixmap(pixmap)
            else:
                icon_label.setText("🖼️")
                icon_label.setAlignment(Qt.AlignCenter)
                icon_label.setStyleSheet("font-size: 48px;")
            icon_label.setFixedSize(64, 64)
            card_layout.addWidget(icon_label)

            # Bloc texte central (nom + description forcée sur au moins 3 lignes)
            text_layout = QVBoxLayout()
            text_layout.setSpacing(8)
            text_layout.setContentsMargins(0, 0, 0, 0)

            name_label = QLabel(filt.name)
            name_label.setFont(QFont("Segoe UI", 13, QFont.Bold))
            name_label.setWordWrap(True)
            name_label.setStyleSheet("color: #1f2937;")
            text_layout.addWidget(name_label)

            # Description : forcée à 3 lignes minimum + multi-lignes si plus long
            desc = filt.description if hasattr(filt, 'description') else "Description non fournie pour ce filtre"
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setMinimumHeight(60)  # Force au moins 3 lignes visibles même si texte court
            desc_label.setStyleSheet("""
                color: #555;
                font-size: 12px;
                line-height: 1.5;
                min-height: 60px;  /* 3 lignes minimum */
            """)
            text_layout.addWidget(desc_label)

            card_layout.addLayout(text_layout, stretch=1)

            # Bouton Appliquer
            apply_btn = QPushButton("Appliquer")
            apply_btn.setFixedSize(120, 44)
            apply_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3b82f6;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                }
                QPushButton:hover {
                    background-color: #2563eb;
                }
                QPushButton:pressed {
                    background-color: #1d4ed8;
                }
            """)
            apply_btn.clicked.connect(lambda checked, f=filt: self.apply_filter(f))
            card_layout.addWidget(apply_btn)

            self.filters_layout.addWidget(card)

    def apply_filter(self, filter_instance):
        if self.filter_manager is None:
            print("Erreur : filter_manager non disponible")
            return

        params = filter_instance.get_default_params()

        if params:
            dialog = FilterParamsDialog(filter_instance, self.main_window, self)
            dialog.previewRequested.connect(lambda p: self.preview_filter(filter_instance, p))
            if dialog.exec_() == QDialog.Accepted:
                params = dialog.get_params()
            else:
                return

        success = self.filter_manager.apply_filter(filter_instance, params)

        if success:
            if hasattr(self.main_window, 'applied_filters'):
                self.main_window.applied_filters.append((filter_instance.name, params.copy()))

            img = self.main_window.image_manager.get_current()
            if img is not None:
                self.main_window.viewer.display_image(img)

                if self.main_window.current_image_index >= 0:
                    self.main_window.loaded_images[self.main_window.current_image_index] = img.copy()
                    filename = self.main_window.image_filenames[self.main_window.current_image_index] if self.main_window.current_image_index < len(self.main_window.image_filenames) else "inconnue"
                    print(f"Filtre '{filter_instance.name}' appliqué et enregistré sur : {filename}")

        else:
            print(f"Échec application filtre : {filter_instance.name}")

    def preview_filter(self, filter_instance, params):
        current_img = self.main_window.image_manager.get_current()
        if current_img is None:
            return

        try:
            preview_img = filter_instance.apply(current_img.copy(), params)
            if preview_img is not None:
                self.main_window.viewer.display_image(preview_img)
        except Exception as e:
            print(f"Erreur preview : {e}")