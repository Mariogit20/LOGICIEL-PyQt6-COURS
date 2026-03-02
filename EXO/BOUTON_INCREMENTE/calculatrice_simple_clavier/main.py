import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# # -----------------------------------------

# --- FONCTION MAGIQUE POUR PYINSTALLER (CORRIGÉE) ---
def chemin_ressource(chemin_relatif):
    """ Obtenir le chemin absolu vers la ressource, fonctionne pour le dev et pour PyInstaller """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        chemin_base = sys._MEIPASS
    except Exception:
        # Au lieu de ".", on prend le dossier exact où se trouve ce fichier Python (__file__)
        chemin_base = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(chemin_base, chemin_relatif)
# ----------------------------------------------------

class Calculatrice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice Clavier")
        self.setFixedSize(300, 400)
        
        self.load_icon()        
        self.load_style() 
                
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        self.layout = QGridLayout()
        widget_central.setLayout(self.layout)
        
        self.creer_interface()

    def creer_interface(self):
        self.ecran = QLineEdit()
        self.ecran.setFixedHeight(60)
        self.ecran.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ecran.setReadOnly(True)
        self.layout.addWidget(self.ecran, 0, 0, 1, 4)

        boutons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for texte, ligne, colonne in boutons:
            bouton = QPushButton(texte)
            bouton.setFixedSize(60, 60)
            
            if texte in ['/', '*', '-', '+', '=']:
                bouton.setProperty("class", "operateur")
            elif texte == 'C':
                bouton.setProperty("class", "effacer")
            else:
                bouton.setProperty("class", "chiffre")
                
            bouton.clicked.connect(self.action_bouton)
            self.layout.addWidget(bouton, ligne, colonne)

    def action_bouton(self):
        valeur = self.sender().text()
        if valeur == 'C':
            self.ecran.clear()
        elif valeur == '=':
            self.calculer_resultat()
        else:
            self.ajouter_caractere(valeur)

    def keyPressEvent(self, event):
        touche = event.text()
        
        if touche in "0123456789+-*/":
            self.ajouter_caractere(touche)
            
        elif event.key() in (Qt.Key.Key_Enter, Qt.Key.Key_Return):
            self.calculer_resultat()
            
        elif event.key() == Qt.Key.Key_Backspace:
            texte_actuel = self.ecran.text()
            self.ecran.setText(texte_actuel[:-1]) 
            
        elif event.key() == Qt.Key.Key_Escape:
            self.ecran.clear()

    def ajouter_caractere(self, caractere):
        texte_actuel = self.ecran.text()
        if texte_actuel == "Erreur":
            texte_actuel = ""
        self.ecran.setText(texte_actuel + caractere)

    def calculer_resultat(self):
        try:
            if self.ecran.text():
                resultat = eval(self.ecran.text())
                self.ecran.setText(str(resultat))
        except Exception:
            self.ecran.setText("Erreur")
    
    # --- MODIFIÉ POUR UTILISER chemin_ressource ---
    def load_icon(self):
        # On remplace os.path.dirname(__file__) par la fonction magique
        icon_path = chemin_ressource(os.path.join("assets", "images", "favicon.ico"))
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("Icône introuvable :", icon_path)
            
    # --- MODIFIÉ POUR UTILISER chemin_ressource ---
    def load_style(self):
        # On remplace os.path.dirname(__file__) par la fonction magique
        style_path = chemin_ressource(os.path.join("assets", "style.qss"))
        if os.path.exists(style_path):
            with open(style_path, "r", encoding="utf-8") as f:
                self.setStyleSheet(f.read())
        else:
            print("Fichier style introuvable :", style_path)
            
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Calculatrice()
    fenetre.show()
    sys.exit(app.exec())