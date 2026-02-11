# main.py
import sys
from PyQt5.QtWidgets import QApplication, QAction
from ui.main_window import MainWindow


def load_qss(path: str) -> str:
    """Charge un fichier .qss et retourne son contenu"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"Erreur lors du chargement du style {path} : {e}")
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Charger le style par défaut (clair)
    default_style = load_qss("assets/styles/default.qss")
    app.setStyleSheet(default_style)

    # Création de la fenêtre principale
    window = MainWindow()

    # Ajout du switch mode sombre (dans le menu Affichage)
    theme_action = QAction("Activer le mode sombre", window)
    theme_action.setCheckable(True)
    theme_action.toggled.connect(
        lambda checked: app.setStyleSheet(
            load_qss("assets/styles/dark.qss") if checked else load_qss("assets/styles/default.qss")
        )
    )

    # Ajouter au menu Affichage
    if window.menuBar():
        view_menu = window.menuBar().addMenu("Affichage")
        view_menu.addAction(theme_action)

    window.show()
    sys.exit(app.exec_())