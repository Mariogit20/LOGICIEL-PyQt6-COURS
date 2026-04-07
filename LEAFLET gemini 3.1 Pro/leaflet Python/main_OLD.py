import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

def obtenir_chemin_ressource(chemin_relatif):
    """Permet de trouver le chemin des fichiers, même après compilation en .exe"""
    try:
        # Chemin temporaire utilisé par PyInstaller
        chemin_base = sys._MEIPASS
    except Exception:
        # Chemin normal si lancé depuis Python
        chemin_base = os.path.abspath(".")
    return os.path.join(chemin_base, chemin_relatif)

class CartographieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Titre et taille de la fenêtre
        self.setWindowTitle("Explorateur Spatial & Outils SIG")
        self.setGeometry(100, 100, 1280, 720)
        
        # Navigateur intégré
        self.navigateur = QWebEngineView()
        
        # Chargement de la page HTML locale
        chemin_html = obtenir_chemin_ressource("index.html")
        url_locale = QUrl.fromLocalFile(chemin_html)
        
        self.navigateur.setUrl(url_locale)
        self.setCentralWidget(self.navigateur)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = CartographieApp()
    fenetre.show()
    sys.exit(app.exec())