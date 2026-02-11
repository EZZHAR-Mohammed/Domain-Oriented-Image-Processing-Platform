from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PyQt5.QtCore import Qt

class FilterPanel(QWidget):
    def __init__(self, filter_manager, parent=None):
        super().__init__(parent)
        self.filter_manager = filter_manager
        self.current_filter_widgets = []

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Filtres disponibles"))

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.content_widget = QWidget()
        self.filters_layout = QVBoxLayout(self.content_widget)
        self.scroll.setWidget(self.content_widget)

        layout.addWidget(self.scroll)
        self.setLayout(layout)

    def clear(self):
        for i in reversed(range(self.filters_layout.count())):
            widget = self.filters_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        self.current_filter_widgets.clear()

    def load_filters(self, filters_list):
        self.clear()
        for f in filters_list:
            btn = QPushButton(f.name)
            btn.clicked.connect(lambda checked, filt=f: self.apply_filter(filt))
            self.filters_layout.addWidget(btn)
            # On peut ajouter ici un widget de paramètres plus tard