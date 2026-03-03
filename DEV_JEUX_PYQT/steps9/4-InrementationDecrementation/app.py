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
        self.counter_ui()
        
        
    
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
            
    def counter_ui(self):
        main_layout = QVBoxLayout()
        layout = QVBoxLayout()
        
        self.label = QLabel(f"Counter: {self.counter}")
        
        main_layout.addWidget(self.label)
        
        button1 = QPushButton("+")
        button1.clicked.connect(self.increment)
        
        button2 = QPushButton("-")
        button2.clicked.connect(self.decrement)
        
        layout.addWidget(button1)
        layout.addWidget(button2)
        
        main_layout.addLayout(layout)
        
        Widget = QWidget()
        Widget.setLayout(main_layout)
        self.setCentralWidget(Widget)
        
    def increment(self):
        self.counter += 1
        self.label.setText(f"Counter: {self.counter}")
        
    def decrement(self):
        if self.counter > 0:
            self.counter -= 1
            self.label.setText(f"Counter: {self.counter}")

            
    