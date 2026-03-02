from PyQt6.QtWidgets import QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()

        self.add_layouts_vertical()
    
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
    # Création des formulaires
    # ----------------------
    def add_layouts_vertical(self):
        # Création layouts
        layoutvertical = QVBoxLayout()
        
        button1 = QPushButton("Button 1")
        # class pour styliser dans qss
        button1.setObjectName("buttonPrimary")
        
        button2 = QPushButton("Button 2")
        button2.setProperty("class", "button")
        
        button3 = QPushButton("Button 3")
        button3.setProperty("class", "button")
        
        button4 = QPushButton("Button 4")
        button4.setProperty("class", "button")
        
        # Ajout des widgets
        layoutvertical.addWidget(button2)
        layoutvertical.addWidget(button1)
        layoutvertical.addWidget(button3)
        layoutvertical.addWidget(button4)
        
        self.setLayout(layoutvertical)
        
        # Creation de Widget et ajout de la fenêtre
        Widget = QWidget(self)
        Widget.setLayout(layoutvertical)
        
        self.setCentralWidget(Widget)
        
        
        
