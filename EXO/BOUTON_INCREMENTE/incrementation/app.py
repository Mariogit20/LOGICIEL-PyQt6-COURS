import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # CORRECTION 1 : Toujours initialiser les variables d'état en premier
        self.valeur_label = 0
        
        self.setup_window()
        self.load_icon()
        self.load_style()
        self.add_Layouts()
    
    # ----------------------
    # Configuration de la fenêtre
    # ----------------------
    def setup_window(self):
        self.setWindowTitle("My Application")
        self.setFixedSize(1000, 400)
    
    # ----------------------
    # Charger l’icône depuis le fichier
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
            with open(style_path, "r", encoding="utf-8") as f: # Ajout de l'encodage utf-8
                self.setStyleSheet(f.read())
        else:
            print("Fichier style introuvable :", style_path)
            
    # ----------------------
    # Ajouter les layouts QVBOX AND QHBOX
    # ----------------------
    def add_Layouts(self):
        main_layout = QVBoxLayout()
        
        # CORRECTION 2 : On utilise self.label (attribut de classe) et non label (variable locale)
        # J'ai mis str(self.valeur_label) au lieu de "Hello World !" pour plus de cohérence
        self.label = QLabel(str(self.valeur_label))
        self.label.setProperty("class", "labelPrimary")
        
        main_layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        horizontal_layout = QHBoxLayout()

        button1 = QPushButton("Incrémenter +")
        button1.setProperty("class", "button") 
        button1.clicked.connect(self.incrementation)       

        button2 = QPushButton("Décrémenter -")
        button2.setProperty("class", "button")
        button2.clicked.connect(self.decrementation) 

        horizontal_layout.addWidget(button1)
        horizontal_layout.addWidget(button2)
         
        main_layout.addLayout(horizontal_layout)

        # CORRECTION 3 : Minuscule pour le nom de variable (bonne pratique Python)
        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)
        
        self.setCentralWidget(central_widget)
        
    def incrementation(self):
        self.valeur_label += 1 # Plus propre que self.valeur_label = self.valeur_label + 1
        self.label.setText(str(self.valeur_label))
        
    def decrementation(self):    
        self.valeur_label -= 1   
        self.label.setText(str(self.valeur_label))        

# # CORRECTION 4 : Ajout de la boucle d'exécution indispensable pour lancer l'application
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     fenetre = App()
#     fenetre.show()
#     sys.exit(app.exec())