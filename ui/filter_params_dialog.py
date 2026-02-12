# ui/filter_params_dialog.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QFormLayout
from PyQt5.QtCore import Qt, pyqtSignal


class FilterParamsDialog(QDialog):
    previewRequested = pyqtSignal(dict)  # Pour preview live

    def __init__(self, filter_instance, main_window, parent=None):
        super().__init__(parent)
        self.filter_instance = filter_instance
        self.main_window = main_window  # Pour accéder à viewer et image_manager en preview

        self.setWindowTitle(f"Paramètres - {filter_instance.name}")
        self.setMinimumWidth(350)

        layout = QVBoxLayout()
        form = QFormLayout()

        self.params = filter_instance.get_default_params().copy()

        # Sliders dynamiques
        for key, default_value in self.params.items():
            label = QLabel(key.capitalize().replace("_", " "))

            if isinstance(default_value, int):
                slider = QSlider(Qt.Horizontal)
                slider.setRange(0, 100)  # Ajustable selon filtre
                slider.setValue(default_value)
                slider.valueChanged.connect(lambda v, k=key: self.update_and_preview(k, v))
                form.addRow(label, slider)

            elif isinstance(default_value, float):
                slider = QSlider(Qt.Horizontal)
                slider.setRange(0, 1000)
                slider.setValue(int(default_value * 100))
                slider.valueChanged.connect(lambda v, k=key: self.update_and_preview(k, v / 100.0))
                form.addRow(label, slider)

        layout.addLayout(form)

        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Appliquer")
        apply_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(apply_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

    def update_and_preview(self, key, value):
        self.params[key] = value
        self.previewRequested.emit(self.params)

    def get_params(self):
        return self.params