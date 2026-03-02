from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.action_boutton()
    
    # ----------------------
    # Configuration de la fenêtre
    # ----------------------
    def setup_window(self):
        self.setWindowTitle("My Application")
        self.setFixedSize(1000, 400)
    
    # ----------------------
    # Charger l’icône sut le fichier
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
    # Ajouter le message de bienvenue
    # ----------------------
    def action_boutton(self):
        layout = QVBoxLayout()
        
        # Création du label comme attribut de la classe
        self.label = QLabel("Bienvenue dans votre Application !")
        self.label.setProperty("class", "formLabel")
        
        # Création du bouton
        button = QPushButton("Boutton")
        button.setProperty("class", "button")
        
        # Connexion du signal clicked à une méthode
        button.clicked.connect(self.bouton_clicked)
        
        layout.addWidget(self.label)
        layout.addWidget(button)
        
        Widget = QWidget(self)
        Widget.setLayout(layout)
        
        self.setCentralWidget(Widget)
        
    # ----------------------
    # Méthode appelée lorsque le bouton est cliqué
    # ----------------------
    def bouton_clicked(self):
        print("Le bouton a été cliqué !")
        
        self.label.setText("Hello World !")