import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QPushButton,
    QLineEdit
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt


def resource_path(relative_path):
    """
    Fonctionne en local ET avec PyInstaller
    """
    try:
        base_path = sys._MEIPASS  # quand c'est compilé
    except AttributeError:
        base_path = os.path.dirname(os.path.abspath(__file__))  # en local

    return os.path.join(base_path, relative_path)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.create_calculator()

    # ----------------------
    # Configuration fenêtre
    # ----------------------
    def setup_window(self):
        self.setWindowTitle("Calculatrice")
        # self.setFixedSize(350, 450)

    # ----------------------
    # Charger icône
    # ----------------------
    def load_icon(self):
        icon_path = resource_path("assets/images/favicon.ico")

        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("Icône introuvable :", icon_path)

    # ----------------------
    # Charger style QSS
    # ----------------------
    def load_style(self):
        style_path = resource_path("assets/style.qss")

        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print("Fichier style introuvable :", style_path)

    # ----------------------
    # Création calculatrice
    # ----------------------
    def create_calculator(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        grid_layout = QGridLayout()

        # Écran d'affichage
        self.display = QLineEdit()
        self.display.setProperty("class", "calculator-display")
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        main_layout.addWidget(self.display)

        # Boutons
        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('C', 3, 2), ('+', 3, 3),
            ('=', 4, 0, 1, 4)
        ]

        for button in buttons:
            text, row, col, *span = button
            rowspan = span[0] if len(span) > 0 else 1
            colspan = span[1] if len(span) > 1 else 1

            btn = QPushButton(text)
            btn.setProperty("class", "calculator-button")
            btn.setFixedHeight(50)
            btn.clicked.connect(self.on_button_clicked)

            grid_layout.addWidget(btn, row, col, rowspan, colspan)

        main_layout.addLayout(grid_layout)
        central_widget.setLayout(main_layout)

    # ----------------------
    # Gestion clic boutons
    # ----------------------
    def on_button_clicked(self):
        text = self.sender().text()

        if text == "C":
            self.display.clear()

        elif text == "=":
            try:
                result = eval(self.display.text())
                self.display.setText(str(result))
            except Exception:
                self.display.setText("Erreur")

        else:
            self.display.setText(self.display.text() + text)