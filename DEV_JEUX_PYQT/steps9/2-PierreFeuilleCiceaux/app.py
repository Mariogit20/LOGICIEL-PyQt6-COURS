from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QFrame
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect
import os
import random


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.load_icon()
        self.load_style()

        self.mode = None
        self.score_joueur1 = 0
        self.score_joueur2 = 0
        self.choix_joueur1 = None
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("Pierre Feuille Ciseaux")
        self.setFixedSize(1000, 500)

    def load_icon(self):
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "images", "favicon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

    def load_style(self):
        style_path = os.path.join(os.path.dirname(__file__), "assets", "style.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
        else:
            print("Fichier style introuvable :", style_path)

    def setup_ui(self):
        # ── Titre ──────────────────────────────────────────────────────────────
        self.titre_label = QLabel("✊  Pierre  •  Feuille  •  Ciseaux  ✌️", self)
        self.titre_label.setObjectName("titre")
        self.titre_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre_label.setGeometry(0, 28, 1000, 48)

        # ── Séparateur décoratif ───────────────────────────────────────────────
        self.sep = QFrame(self)
        self.sep.setFrameShape(QFrame.Shape.HLine)
        self.sep.setObjectName("separator")
        self.sep.setGeometry(200, 82, 600, 2)

        # ── Résultat ──────────────────────────────────────────────────────────
        self.resultat_label = QLabel("Choisissez votre mode de jeu", self)
        self.resultat_label.setObjectName("resultat")
        self.resultat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.resultat_label.setGeometry(100, 95, 800, 70)
        self.resultat_label.setWordWrap(True)

        # ── Score ──────────────────────────────────────────────────────────────
        self.score_label = QLabel("Score :  0  —  0", self)
        self.score_label.setObjectName("score")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setGeometry(300, 170, 400, 40)

        # ── Boutons mode ──────────────────────────────────────────────────────
        self.btn_ordi = QPushButton("🖥️  Joueur  vs  Ordinateur", self)
        self.btn_joueur = QPushButton("👥  Joueur  vs  Joueur", self)
        self.btn_ordi.setObjectName("btnMode")
        self.btn_joueur.setObjectName("btnMode")
        self.btn_ordi.setGeometry(215, 250, 260, 56)
        self.btn_joueur.setGeometry(525, 250, 260, 56)
        self.btn_ordi.clicked.connect(lambda: self.set_mode("ordi"))
        self.btn_joueur.clicked.connect(lambda: self.set_mode("joueur"))

        # ── Boutons jeu ───────────────────────────────────────────────────────
        self.btn_pierre  = QPushButton("✊  Pierre",  self)
        self.btn_papier  = QPushButton("🖐️  Papier",  self)
        self.btn_ciseaux = QPushButton("✌️  Ciseaux", self)
        for btn, name in [
            (self.btn_pierre,  "btnPierre"),
            (self.btn_papier,  "btnPapier"),
            (self.btn_ciseaux, "btnCiseaux"),
        ]:
            btn.setObjectName(name)

        self.btn_pierre.setGeometry(200, 250, 170, 60)
        self.btn_papier.setGeometry(415, 250, 170, 60)
        self.btn_ciseaux.setGeometry(630, 250, 170, 60)

        for btn in (self.btn_pierre, self.btn_papier, self.btn_ciseaux):
            btn.hide()

        self.btn_pierre.clicked.connect(lambda: self.jouer("Pierre"))
        self.btn_papier.clicked.connect(lambda: self.jouer("Papier"))
        self.btn_ciseaux.clicked.connect(lambda: self.jouer("Ciseaux"))

        # ── Bouton retour ─────────────────────────────────────────────────────
        self.btn_retour = QPushButton("⟵  Retour au menu", self)
        self.btn_retour.setObjectName("btnRetour")
        self.btn_retour.setGeometry(370, 370, 260, 46)
        self.btn_retour.hide()
        self.btn_retour.clicked.connect(self.reset_menu)

    # ── Logique ────────────────────────────────────────────────────────────────

    def set_mode(self, mode):
        self.mode = mode
        label = "🖥️  Mode : Joueur vs Ordinateur" if mode == "ordi" else "👥  Mode : Joueur vs Joueur"
        self.resultat_label.setText(label)
        self.btn_ordi.hide()
        self.btn_joueur.hide()
        for btn in (self.btn_pierre, self.btn_papier, self.btn_ciseaux):
            btn.show()
        self.btn_retour.show()

    def jouer(self, choix):
        if self.mode == "ordi":
            choix_j1 = choix
            choix_j2 = random.choice(["Pierre", "Papier", "Ciseaux"])
        else:
            if not self.choix_joueur1:
                self.choix_joueur1 = choix
                self.resultat_label.setText("🎮  Joueur 2, à vous de choisir !")
                return
            else:
                choix_j1 = self.choix_joueur1
                choix_j2 = choix
                self.choix_joueur1 = None

        # Déterminer le résultat
        if choix_j1 == choix_j2:
            resultat = "🤝  Égalité !"
        elif (
            (choix_j1 == "Pierre"  and choix_j2 == "Ciseaux") or
            (choix_j1 == "Papier"  and choix_j2 == "Pierre")  or
            (choix_j1 == "Ciseaux" and choix_j2 == "Papier")
        ):
            resultat = "🎉  Joueur 1 gagne !"
            self.score_joueur1 += 1
        else:
            resultat = ("🎉  Joueur 2 gagne !" if self.mode == "joueur"
                        else "💻  L'ordinateur gagne !")
            self.score_joueur2 += 1

        emoji = {"Pierre": "✊", "Papier": "🖐️", "Ciseaux": "✌️"}
        self.resultat_label.setText(
            f"{emoji[choix_j1]} {choix_j1}  vs  {emoji[choix_j2]} {choix_j2}\n{resultat}"
        )
        self.score_label.setText(
            f"Score :  {self.score_joueur1}  —  {self.score_joueur2}"
        )

    def reset_menu(self):
        """Réinitialise tout et retourne au menu principal."""
        self.mode = None
        self.score_joueur1 = 0
        self.score_joueur2 = 0
        self.choix_joueur1 = None

        self.resultat_label.setText("Choisissez votre mode de jeu")
        self.score_label.setText("Score :  0  —  0")

        for btn in (self.btn_pierre, self.btn_papier, self.btn_ciseaux):
            btn.hide()
        self.btn_retour.hide()
        self.btn_ordi.show()
        self.btn_joueur.show()


