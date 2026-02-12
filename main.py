# main.py
import sys
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtGui import QFont, QIcon
from ui.main_window import MainWindow


def load_qss(path: str) -> str:
    """Charge un fichier .qss silencieusement (retourne vide si absent ou erreur)"""
    try:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    except Exception:
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ───────────────────────────────────────────────
    # Police globale moderne (Segoe UI ou fallback)
    # ───────────────────────────────────────────────
    font = QFont("Segoe UI", 10)
    font.setStyleHint(QFont.SansSerif)
    app.setFont(font)

    # ───────────────────────────────────────────────
    # Thème initial = clair (light ou default)
    # ───────────────────────────────────────────────
    light_theme = load_qss("assets/styles/light.qss") or load_qss("assets/styles/default.qss")
    if light_theme:
        app.setStyleSheet(light_theme)

    # ───────────────────────────────────────────────
    # Icône de l'application (optionnel)
    # ───────────────────────────────────────────────
    try:
        app.setWindowIcon(QIcon("assets/icon.png"))
    except Exception:
        pass  # Silencieux

    # Création de la fenêtre principale
    window = MainWindow()

    # ───────────────────────────────────────────────
    # Switch thème clair/sombre avec texte dynamique
    # ───────────────────────────────────────────────
    theme_action = QAction("Passer en mode sombre", window)
    theme_action.setCheckable(True)
    theme_action.setChecked(False)  # Démarre en clair

    def toggle_theme(checked):
        if checked:
            dark_theme = load_qss("assets/styles/dark.qss")
            if dark_theme:
                app.setStyleSheet(dark_theme)
                theme_action.setText("Passer en mode clair")
            else:
                print("Fichier dark.qss introuvable ou vide")
        else:
            light_theme = load_qss("assets/styles/light.qss") or load_qss("assets/styles/default.qss")
            if light_theme:
                app.setStyleSheet(light_theme)
                theme_action.setText("Passer en mode sombre")

    theme_action.toggled.connect(toggle_theme)

    # Ajout au menu Affichage
    view_menu = window.menuBar().addMenu("Affichage")
    view_menu.addAction(theme_action)

    # ───────────────────────────────────────────────
    # Lancement
    # ───────────────────────────────────────────────
    window.show()
    sys.exit(app.exec_())