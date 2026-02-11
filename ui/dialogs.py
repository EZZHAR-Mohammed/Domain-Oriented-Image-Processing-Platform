from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFormLayout, QSpinBox, QDoubleSpinBox


class FilterParamsDialog(QDialog):
    """Dialogue générique pour régler les paramètres d'un filtre"""

    def __init__(self, filter_obj, parent=None):
        super().__init__(parent)
        self.filter = filter_obj
        self.setWindowTitle(f"Paramètres - {filter_obj.name}")
        self.params = filter_obj.get_default_params().copy()

        layout = QVBoxLayout()
        form = QFormLayout()

        # Exemple : on affiche les params par défaut (à étendre selon filtre)
        for key, value in self.params.items():
            if isinstance(value, int):
                spin = QSpinBox()
                spin.setValue(value)
                spin.valueChanged.connect(lambda v, k=key: self.params.update({k: v}))
                form.addRow(key, spin)
            elif isinstance(value, float):
                spin = QDoubleSpinBox()
                spin.setValue(value)
                spin.setSingleStep(0.1)
                spin.valueChanged.connect(lambda v, k=key: self.params.update({k: v}))
                form.addRow(key, spin)

        layout.addLayout(form)

        btn_ok = QPushButton("Appliquer")
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def get_params(self):
        return self.params