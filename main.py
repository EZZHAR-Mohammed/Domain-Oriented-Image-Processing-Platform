import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow


def load_qss(path: str) -> str:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Thème par défaut = clair
    app.setStyleSheet(load_qss("assets/styles/default.qss"))

    window = MainWindow()

    # Switch thème rapide (optionnel – via menu Affichage)
    from PyQt5.QtWidgets import QAction
    theme_act = QAction("Mode sombre", window, checkable=True)
    theme_act.toggled.connect(lambda checked: app.setStyleSheet(
        load_qss("assets/styles/dark.qss") if checked else load_qss("assets/styles/default.qss")
    ))
    window.menuBar().addMenu("Affichage").addAction(theme_act)

    window.show()
    sys.exit(app.exec_())