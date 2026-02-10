import sys
from PyQt5.QtWidgets import QApplication, QAction
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow

def load_stylesheet(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except Exception:
        return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("assets/styles/default.qss"))

    window = MainWindow()

    # Switch thème
    theme_action = QAction("Activer Mode Sombre", window)
    theme_action.setCheckable(True)
    theme_action.toggled.connect(lambda checked: 
        app.setStyleSheet(load_stylesheet("assets/styles/dark.qss") if checked 
                          else load_stylesheet("assets/styles/default.qss")))
    view_menu = window.menuBar().addMenu("Affichage")
    view_menu.addAction(theme_action)

    window.show()
    sys.exit(app.exec_())