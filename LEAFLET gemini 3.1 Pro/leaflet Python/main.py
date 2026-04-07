import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineSettings
from PyQt6.QtCore import QUrl

def obtenir_chemin_ressource(chemin_relatif):
    try:
        chemin_base = sys._MEIPASS
    except Exception:
        chemin_base = os.path.abspath(".")
    return os.path.join(chemin_base, chemin_relatif)

class CartographieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Explorateur Spatial - Application SIG")
        self.setGeometry(100, 100, 1280, 720)
        
        self.navigateur = QWebEngineView()
        
        # 1. Autorisations réseau locales
        parametres = self.navigateur.settings()
        parametres.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessRemoteUrls, True)
        parametres.setAttribute(QWebEngineSettings.WebAttribute.LocalContentCanAccessFileUrls, True)
        
        # 2. CORRECTION DU BLOCAGE (403) : Définir l'identité du logiciel
        profil = self.navigateur.page().profile()
        profil.setHttpUserAgent("LogicielExplorateurSpatial/1.0 (Application PyQt6 Bureau)")
        
        # 3. Chargement de l'interface graphique
        chemin_html = obtenir_chemin_ressource("index.html")
        url_locale = QUrl.fromLocalFile(chemin_html)
        
        self.navigateur.setUrl(url_locale)
        self.setCentralWidget(self.navigateur)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = CartographieApp()
    fenetre.show()
    sys.exit(app.exec())