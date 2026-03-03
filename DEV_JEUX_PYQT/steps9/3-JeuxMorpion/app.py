from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
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
        self.plateau = [""] * 9
        self.tour = "X"  # X = Joueur 1, O = Joueur 2 / Ordinateur
        self.partie_terminee = False
        self.setup_ui()

    def setup_window(self):
        self.setWindowTitle("Morpion")
        self.setFixedSize(1000, 580)

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
        self.titre_label = QLabel("❌  Morpion  •  Tic-Tac-Toe  ⭕", self)
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
        self.resultat_label.setGeometry(100, 95, 800, 50)
        self.resultat_label.setWordWrap(True)

        # ── Score ──────────────────────────────────────────────────────────────
        self.score_label = QLabel("Score :  0  —  0", self)
        self.score_label.setObjectName("score")
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setGeometry(300, 150, 400, 40)

        # ── Boutons mode ──────────────────────────────────────────────────────
        self.btn_ordi = QPushButton("🖥️  Joueur  vs  Ordinateur", self)
        self.btn_joueur = QPushButton("👥  Joueur  vs  Joueur", self)
        self.btn_ordi.setObjectName("btnMode")
        self.btn_joueur.setObjectName("btnMode")
        self.btn_ordi.setGeometry(215, 280, 260, 56)
        self.btn_joueur.setGeometry(525, 280, 260, 56)
        self.btn_ordi.clicked.connect(lambda: self.set_mode("ordi"))
        self.btn_joueur.clicked.connect(lambda: self.set_mode("joueur"))

        # ── Grille 3x3 ────────────────────────────────────────────────────────
        self.cellules = []
        cell_size = 110
        grid_x = (1000 - 3 * cell_size - 2 * 8) // 2
        grid_y = 195

        for i in range(9):
            row, col = divmod(i, 3)
            btn = QPushButton("", self)
            btn.setObjectName("btnCell")
            btn.setGeometry(grid_x + col * (cell_size + 8),
                            grid_y + row * (cell_size + 8),
                            cell_size, cell_size)
            btn.clicked.connect(lambda checked, idx=i: self.jouer(idx))
            btn.hide()
            self.cellules.append(btn)

        # ── Bouton Rejouer ────────────────────────────────────────────────────
        self.btn_rejouer = QPushButton("🔄  Rejouer", self)
        self.btn_rejouer.setObjectName("btnRejouer")
        self.btn_rejouer.setGeometry(370, 535, 130, 38)
        self.btn_rejouer.hide()
        self.btn_rejouer.clicked.connect(self.nouvelle_partie)

        # ── Bouton retour ─────────────────────────────────────────────────────
        self.btn_retour = QPushButton("⟵  Retour au menu", self)
        self.btn_retour.setObjectName("btnRetour")
        self.btn_retour.setGeometry(520, 535, 200, 38)
        self.btn_retour.hide()
        self.btn_retour.clicked.connect(self.reset_menu)

    # ── Logique ────────────────────────────────────────────────────────────────

    def set_mode(self, mode):
        self.mode = mode
        self.btn_ordi.hide()
        self.btn_joueur.hide()
        for btn in self.cellules:
            btn.show()
        self.btn_retour.show()
        self.btn_rejouer.show()
        self.nouvelle_partie()

    def nouvelle_partie(self):
        self.plateau = [""] * 9
        self.tour = "X"
        self.partie_terminee = False
        for btn in self.cellules:
            btn.setText("")
            btn.setObjectName("btnCell")
            btn.setEnabled(True)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
        self._update_tour_label()

    def _update_tour_label(self):
        if self.mode == "ordi":
            if self.tour == "X":
                self.resultat_label.setText("❌  Tour du Joueur 1 (X)")
            else:
                self.resultat_label.setText("💻  Tour de l'Ordinateur (O)")
        else:
            if self.tour == "X":
                self.resultat_label.setText("❌  Tour du Joueur 1 (X)")
            else:
                self.resultat_label.setText("⭕  Tour du Joueur 2 (O)")

    def jouer(self, idx):
        if self.partie_terminee or self.plateau[idx] != "":
            return

        self.plateau[idx] = self.tour
        self._update_cell(idx)

        gagnant = self._verifier_gagnant()
        if gagnant:
            self._fin_partie(gagnant)
            return
        if "" not in self.plateau:
            self._fin_partie("nul")
            return

        self.tour = "O" if self.tour == "X" else "X"

        if self.mode == "ordi" and self.tour == "O":
            self._update_tour_label()
            self._tour_ordi()
        else:
            self._update_tour_label()

    def _tour_ordi(self):
        # Stratégie simple : gagner > bloquer > centre > coin > autre
        coup = self._meilleur_coup()
        self.plateau[coup] = "O"
        self._update_cell(coup)

        gagnant = self._verifier_gagnant()
        if gagnant:
            self._fin_partie(gagnant)
            return
        if "" not in self.plateau:
            self._fin_partie("nul")
            return

        self.tour = "X"
        self._update_tour_label()

    def _meilleur_coup(self):
        # Gagner
        for i in range(9):
            if self.plateau[i] == "":
                self.plateau[i] = "O"
                if self._verifier_gagnant() == "O":
                    self.plateau[i] = ""
                    return i
                self.plateau[i] = ""
        # Bloquer
        for i in range(9):
            if self.plateau[i] == "":
                self.plateau[i] = "X"
                if self._verifier_gagnant() == "X":
                    self.plateau[i] = ""
                    return i
                self.plateau[i] = ""
        # Centre
        if self.plateau[4] == "":
            return 4
        # Coins
        coins = [i for i in [0, 2, 6, 8] if self.plateau[i] == ""]
        if coins:
            return random.choice(coins)
        # Reste
        libres = [i for i in range(9) if self.plateau[i] == ""]
        return random.choice(libres)

    def _update_cell(self, idx):
        btn = self.cellules[idx]
        if self.plateau[idx] == "X":
            btn.setText("❌")
            btn.setObjectName("btnCellX")
        else:
            btn.setText("⭕")
            btn.setObjectName("btnCellO")
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    def _verifier_gagnant(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
            (0, 4, 8), (2, 4, 6),              # diagonales
        ]
        for a, b, c in combos:
            if self.plateau[a] and self.plateau[a] == self.plateau[b] == self.plateau[c]:
                # Surligner les cellules gagnantes
                for idx in (a, b, c):
                    self.cellules[idx].setObjectName("btnCellWin")
                    self.cellules[idx].style().unpolish(self.cellules[idx])
                    self.cellules[idx].style().polish(self.cellules[idx])
                return self.plateau[a]
        return None

    def _fin_partie(self, resultat):
        self.partie_terminee = True
        for btn in self.cellules:
            btn.setEnabled(False)

        if resultat == "nul":
            self.resultat_label.setText("🤝  Égalité !")
        elif resultat == "X":
            self.score_joueur1 += 1
            self.resultat_label.setText("🎉  Joueur 1 gagne !")
        else:
            self.score_joueur2 += 1
            if self.mode == "ordi":
                self.resultat_label.setText("💻  L'ordinateur gagne !")
            else:
                self.resultat_label.setText("🎉  Joueur 2 gagne !")

        self.score_label.setText(
            f"Score :  {self.score_joueur1}  —  {self.score_joueur2}"
        )

    def reset_menu(self):
        self.mode = None
        self.score_joueur1 = 0
        self.score_joueur2 = 0
        self.plateau = [""] * 9
        self.tour = "X"
        self.partie_terminee = False

        self.resultat_label.setText("Choisissez votre mode de jeu")
        self.score_label.setText("Score :  0  —  0")

        for btn in self.cellules:
            btn.hide()
            btn.setText("")
        self.btn_retour.hide()
        self.btn_rejouer.hide()
        self.btn_ordi.show()
        self.btn_joueur.show()