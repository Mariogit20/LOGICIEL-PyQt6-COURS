from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget
from PyQt6.QtGui import QIcon
import os

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.setup_ui()  # Création de l'interface principale
    
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
    # Créer l'interface principale avec page d'accueil et bouton
    # ----------------------
    def setup_ui(self):
        # StackedWidget pour gérer plusieurs pages
        self.pages = QStackedWidget()
        
        # Créer les pages séparément
        self.create_home_page()
        self.create_page2()
        
        # Ajouter les pages au StackedWidget
        self.pages.addWidget(self.page_home)
        self.pages.addWidget(self.page2)
        
        # Définir le StackedWidget comme widget central
        self.setCentralWidget(self.pages)

    # ----------------------
    # Création de la page d'accueil
    # ----------------------
    def create_home_page(self):
        self.page_home = QWidget()
        layout_home = QVBoxLayout()
        
        self.welcome_label = QLabel("Bienvenue dans votre ToDo List !")
        self.welcome_label.setStyleSheet("color: white; font-size: 24px;")
        layout_home.addWidget(self.welcome_label)
        
        button = QPushButton("Aller à la Page 2")
        button.setProperty("class", "button")
        button.clicked.connect(self.show_page2)
        layout_home.addWidget(button)
        
        self.page_home.setLayout(layout_home)

    # ----------------------
    # Création de la page 2
    # ----------------------
    def create_page2(self):
        self.page2 = QWidget()
        layout_page2 = QVBoxLayout()
            
        label_page2 = QLabel("Ceci est la deuxième page !")
        label_page2.setStyleSheet("color: white; font-size: 24px;")
        layout_page2.addWidget(label_page2)
            
        back_button = QPushButton("Retour à l'accueil")
        back_button.setProperty("class", "button")
        back_button.clicked.connect(self.show_home)
        layout_page2.addWidget(back_button)
            
        self.page2.setLayout(layout_page2)

    # ----------------------
    # Méthodes pour changer de page
    # ----------------------
    def show_page2(self):
        self.pages.setCurrentWidget(self.page2)

    def show_home(self):
        self.pages.setCurrentWidget(self.page_home)