import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLineEdit, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# class Calculatrice(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Calculatrice Simple")
#         self.setFixedSize(300, 400)
        
#         # Création du widget central et du layout en grille

class Calculatrice(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculatrice Simple")
        self.setFixedSize(300, 400)
        
        self.load_icon()        
        
        # --- AJOUT DU STYLE QSS ICI ---
        style_css = """
        QWidget { background-color: #1e1e1e; }
        QLineEdit { background-color: transparent; border: none; font-size: 45px; color: #ffffff; padding-right: 15px; margin-bottom: 10px; }
        QPushButton { background-color: #333333; color: #ffffff; font-size: 24px; font-weight: bold; border: none; border-radius: 30px; }
        QPushButton:hover { background-color: #4d4d4d; }
        QPushButton:pressed { background-color: #a6a6a6; }
        """
        self.setStyleSheet(style_css)
        # ------------------------------
        
        # Création du widget central et du layout en grille
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        self.layout = QGridLayout()
        widget_central.setLayout(self.layout)
        
        self.creer_interface()

    def creer_interface(self):
        # 1. L'écran d'affichage (QLineEdit)
        self.ecran = QLineEdit()
        self.ecran.setFixedHeight(60)
        self.ecran.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.ecran.setReadOnly(True) # Empêche la saisie directe au clavier pour cet exemple
        
        # Ajout de l'écran : Ligne 0, Colonne 0, s'étend sur 1 ligne et 4 colonnes
        self.layout.addWidget(self.ecran, 0, 0, 1, 4)

        # 2. Configuration des boutons (Texte, Ligne, Colonne)
        boutons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        # 3. Génération dynamique des boutons
        for texte, ligne, colonne in boutons:
            bouton = QPushButton(texte)
            bouton.setFixedSize(60, 60)
            
            # On connecte chaque bouton à la même méthode
            bouton.clicked.connect(self.action_bouton)
            
            # On place le bouton dans la grille
            self.layout.addWidget(bouton, ligne, colonne)

    def action_bouton(self):
        # self.sender() permet de savoir quel bouton a déclenché l'événement
        bouton_clique = self.sender()
        valeur = bouton_clique.text()

        if valeur == 'C':
            # Effacer l'écran
            self.ecran.clear()
            
        elif valeur == '=':
            # Calculer le résultat
            try:
                # eval() analyse et exécute la chaîne de caractères comme du code Python
                resultat = eval(self.ecran.text())
                self.ecran.setText(str(resultat))
            except Exception:
                # Gestion des erreurs (ex: division par zéro ou syntaxe invalide)
                self.ecran.setText("Erreur")
                
        else:
            # Ajouter le chiffre ou l'opérateur à l'écran
            texte_actuel = self.ecran.text()
            
            # Réinitialiser si l'écran affiche une erreur
            if texte_actuel == "Erreur":
                texte_actuel = ""
                
            self.ecran.setText(texte_actuel + valeur)

    
    # ----------------------
    # Charger l’icône depuis le fichier
    # ----------------------
    def load_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "images", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            print("Icône introuvable :", icon_path)
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Calculatrice()
    fenetre.show()
    sys.exit(app.exec())