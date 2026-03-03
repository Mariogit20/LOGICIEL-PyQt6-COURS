from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget
from PyQt6.QtGui import QIcon
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.counter = 0  
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.add_welcome_message()
        self.layout_buttons_counter()
    
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
    # Ajouter le message de bienvenue
    # ----------------------
    def add_welcome_message(self):
        self.welcome_label = QLabel("Bienvenue dans votre ToDo List !", self)
        self.welcome_label.setStyleSheet("color: white; font-size: 24px;")
        self.welcome_label.adjustSize()
    
    # ----------------------
    # Layout avec boutons + compteur
    # ----------------------
    def layout_buttons_counter(self):
        # Création des widgets
        self.counter_label = QLabel(f"Compteur: {self.counter}")
        self.counter_label.setStyleSheet("color: white; font-size: 20px;")
        
        increment_button = QPushButton("Incrementer")
        decrement_button = QPushButton("Decrementer")
        
        # Connexion des boutons
        increment_button.clicked.connect(self.increment)
        decrement_button.clicked.connect(self.decrement)
        
        # Layout vertical
        layout = QVBoxLayout()
        layout.addWidget(self.welcome_label)
        layout.addWidget(self.counter_label)
        layout.addWidget(increment_button)
        layout.addWidget(decrement_button)
        
        # Widget central
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    # ----------------------
    # Fonctions increment/decrement
    # ----------------------
    def increment(self):
        self.counter += 1
        self.counter_label.setText(f"Compteur: {self.counter}")
    
    def decrement(self):
        if self.counter > 0:   # Vérifie que le compteur est > 0
            self.counter -= 1
            self.counter_label.setText(f"Compteur: {self.counter}")

