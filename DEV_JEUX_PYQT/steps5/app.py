from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.add_grid_layout()

    # ----------------------
    # Configuration de la fenêtre
    # ----------------------
    def setup_window(self):
        self.setWindowTitle("My Application")
        self.setFixedSize(1000, 400)

    # ----------------------
    # Charger l’icône
    # ----------------------
    def load_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "images", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("Icône introuvable :", icon_path)

    # ----------------------
    # Charger le style QSS
    # ----------------------
    def load_style(self):
        style_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print("Fichier style introuvable :", style_path)

    # ----------------------
    # Ajouter le formulaire en grille
    # ----------------------
    def add_grid_layout(self):
        grid = QGridLayout()

        # Labels
        label_name = QLabel("Nom :")
        label_email = QLabel("Email :")
        label_password = QLabel("Password :")

        # Ajouter classe CSS aux labels
        label_name.setProperty("class", "formLabel")
        label_email.setProperty("class", "formLabel")
        label_password.setProperty("class", "formLabel")

        # Champs texte
        input_name = QLineEdit()
        input_email = QLineEdit()
        input_password = QLineEdit()
        input_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Ajouter classe CSS aux champs texte
        input_name.setProperty("class", "formInput")
        input_email.setProperty("class", "formInput")
        input_password.setProperty("class", "formInput")

        # Bouton
        button_login = QPushButton("Login")
        button_login.setProperty("class", "formButton")

        # Ajouter widgets dans la grille
        grid.addWidget(label_name, 0, 0)
        grid.addWidget(input_name, 0, 1)

        grid.addWidget(label_email, 1, 0)
        grid.addWidget(input_email, 1, 1)

        grid.addWidget(label_password, 2, 0)
        grid.addWidget(input_password, 2, 1)

        # Bouton centré sur 2 colonnes
        grid.addWidget(button_login, 3, 0, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Centrer toute la grille
        grid.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(15)

        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)