from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QListWidget
from PyQt5.QtCore import pyqtSignal

class DomainSelectionView(QDialog):
    domainSelected = pyqtSignal(str)

    def __init__(self, domain_manager, parent=None):
        super().__init__(parent)
        self.domain_manager = domain_manager
        self.setWindowTitle("Choisir un domaine d'application")
        self.setMinimumWidth(380)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Sélectionnez le domaine principal :"))

        self.list_widget = QListWidget()
        for name in self.domain_manager.get_domain_names():
            self.list_widget.addItem(name)
        layout.addWidget(self.list_widget)

        btn_ok = QPushButton("Confirmer")
        btn_ok.clicked.connect(self.accept_selection)
        layout.addWidget(btn_ok)

        self.setLayout(layout)

    def accept_selection(self):
        current = self.list_widget.currentItem()
        if current:
            domain_name = current.text()
            self.domainSelected.emit(domain_name)
            self.accept()
        else:
            self.reject()