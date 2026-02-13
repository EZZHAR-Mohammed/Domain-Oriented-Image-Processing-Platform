# ui/filter_card.py
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt


class FilterCard(QFrame):
    def __init__(self, filter_instance, icon_path=None, parent=None):
        super().__init__(parent)
        self.filter_instance = filter_instance
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #f8f9fc;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                padding: 8px;
            }
            QFrame:hover {
                background-color: #e8f0fe;
                border: 1px solid #3b82f6;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(12)

        # Icône (si disponible)
        icon_label = QLabel()
        if icon_path and os.path.exists(icon_path):
            icon_label.setPixmap(QIcon(icon_path).pixmap(48, 48))
        else:
            icon_label.setText("🖼️")  # Emoji par défaut
        icon_label.setFixedSize(48, 48)
        layout.addWidget(icon_label)

        # Infos texte
        text_layout = QVBoxLayout()
        name_label = QLabel(filter_instance.name)
        name_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        text_layout.addWidget(name_label)

        desc = filter_instance.description if hasattr(filter_instance, 'description') else "Filtre standard"
        desc_label = QLabel(desc)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("color: #555;")
        text_layout.addWidget(desc_label)

        layout.addLayout(text_layout)
        layout.addStretch()

        # Bouton Appliquer
        apply_btn = QPushButton("Appliquer")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #2563eb;
            }
        """)
        apply_btn.clicked.connect(self.on_apply_clicked)
        layout.addWidget(apply_btn)

    def on_apply_clicked(self):
        # Émet un signal ou appelle directement la méthode parent
        if hasattr(self.parent(), 'apply_filter'):
            self.parent().apply_filter(self.filter_instance)