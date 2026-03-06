import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QLabel, QMessageBox, 
                             QFrame, QSizePolicy, QSpacerItem)
from PyQt6.QtCore import Qt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

class LogicielCryptage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SecureFolder - Streaming Edition")
        self.resize(550, 400) # Légèrement agrandi pour le texte
        self.setMinimumSize(450, 300)
        
        self.chemin_cible = None
        self.cle = None
        self.fichier_cle = "ma_cle_chacha20.key"
        self.taille_chunk = 64 * 1024  # 64 Ko par morceau
        
        self.initUI()
        self.appliquer_style()
        self.charger_ou_generer_cle()

    def initUI(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        # --- CORRECTION DU TEXTE ICI ---
        texte_titre = (
            "Avec le ChaCha20 pur, un fichier individuel à l'intérieur\n"
            "du dossier peut parfaitement dépasser 256 Go.\n"
            "Aucun Message d'Erreur si un Fichier dépasse 256 Go !"
        )
        titre = QLabel(texte_titre)             
        titre.setObjectName("titre")
        titre.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titre.setWordWrap(True) # Permet au texte de s'adapter à la fenêtre
        layout_principal.addWidget(titre)

        frame_fichier = QFrame()
        frame_fichier.setObjectName("frameFichier")
        layout_fichier = QVBoxLayout(frame_fichier)
        
        self.label_info = QLabel("Aucun dossier sélectionné")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_info.setWordWrap(True)
        
        self.btn_choisir = QPushButton("Parcourir les dossiers...")
        self.btn_choisir.setObjectName("btnChoisir")
        self.btn_choisir.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_choisir.clicked.connect(self.choisir_dossier)
        
        layout_fichier.addWidget(self.label_info)
        layout_fichier.addWidget(self.btn_choisir, alignment=Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(frame_fichier)

        layout_principal.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        layout_boutons = QHBoxLayout()
        layout_boutons.setSpacing(15)

        self.btn_chiffrer = QPushButton("🔒 Chiffrer le dossier")
        self.btn_chiffrer.setObjectName("btnAction")
        self.btn_chiffrer.clicked.connect(self.chiffrer_dossier)
        
        self.btn_dechiffrer = QPushButton("🔓 Déchiffrer le dossier")
        self.btn_dechiffrer.setObjectName("btnAction")
        self.btn_dechiffrer.clicked.connect(self.dechiffrer_dossier)

        self.btn_chiffrer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_dechiffrer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout_boutons.addWidget(self.btn_chiffrer)
        layout_boutons.addWidget(self.btn_dechiffrer)

        layout_principal.addLayout(layout_boutons)
        self.setLayout(layout_principal)

    def appliquer_style(self):
        style = """
            QWidget { background-color: #f4f5f7; font-family: 'Segoe UI', Arial, sans-serif; color: #333333; }
            QLabel#titre { font-size: 16px; font-weight: bold; color: #2980b9; margin-bottom: 10px; }
            QFrame#frameFichier { background-color: #ffffff; border: 2px dashed #bdc3c7; border-radius: 10px; padding: 20px; }
            QLabel { font-size: 14px; color: #7f8c8d; }
            QPushButton { font-size: 14px; font-weight: bold; padding: 10px 20px; border-radius: 6px; border: none; color: white; }
            QPushButton#btnChoisir { background-color: #e74c3c; margin-top: 10px; }
            QPushButton#btnChoisir:hover { background-color: #2980b9; }
            QPushButton#btnChoisir:pressed { background-color: #922b21; }
            QPushButton#btnAction { background-color: #2ecc71; padding: 12px; font-size: 15px; }
            QPushButton#btnAction:hover { background-color: #27ae60; }
            QPushButton#btnAction:pressed { background-color: #1e8449; }
            QPushButton:disabled { background-color: #bdc3c7; color: #7f8c8d; }
        """
        self.setStyleSheet(style)

    def charger_ou_generer_cle(self):
        if not os.path.exists(self.fichier_cle):
            self.cle = os.urandom(32) 
            with open(self.fichier_cle, "wb") as f_cle:
                f_cle.write(self.cle)
        else:
            with open(self.fichier_cle, "rb") as f_cle:
                self.cle = f_cle.read()

    def choisir_dossier(self):
        chemin = QFileDialog.getExistingDirectory(self, "Sélectionner un dossier")
        if chemin:
            self.chemin_cible = chemin
            nom_dossier = os.path.basename(chemin)
            self.label_info.setText(f"<b>Dossier prêt :</b> {nom_dossier}")
            self.label_info.setStyleSheet("color: #2c3e50;")

    def chiffrer_dossier(self):
        if not self.chemin_cible:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord choisir un dossier.")
            return
            
        # Sécurité : on désactive les boutons pendant le travail
        self.btn_chiffrer.setEnabled(False)
        self.btn_dechiffrer.setEnabled(False)
        self.btn_choisir.setEnabled(False)
        QApplication.processEvents()
            
        fichiers_traites = 0
        erreurs = 0

        for racine, sous_dossiers, fichiers in os.walk(self.chemin_cible):
            for nom_fichier in fichiers:
                if nom_fichier.endswith(".enc") or nom_fichier == self.fichier_cle:
                    continue
                    
                chemin_complet = os.path.join(racine, nom_fichier)
                chemin_chiffre = chemin_complet + ".enc"
                
                try:
                    nonce = os.urandom(16)
                    cipher = Cipher(algorithms.ChaCha20(self.cle, nonce), mode=None)
                    encryptor = cipher.encryptor()
                    
                    with open(chemin_complet, "rb") as f_in, open(chemin_chiffre, "wb") as f_out:
                        f_out.write(nonce) 
                        
                        while True:
                            chunk = f_in.read(self.taille_chunk)
                            if not chunk: 
                                break
                            f_out.write(encryptor.update(chunk))
                            
                    os.remove(chemin_complet)
                    fichiers_traites += 1
                    QApplication.processEvents()
                    
                except Exception as e:
                    erreurs += 1
                    print(f"Erreur de chiffrement sur {nom_fichier} : {e}")

        # On réactive les boutons
        self.btn_chiffrer.setEnabled(True)
        self.btn_dechiffrer.setEnabled(True)
        self.btn_choisir.setEnabled(True)
        
        QMessageBox.information(self, "Terminé", f"{fichiers_traites} fichiers chiffrés.\n{erreurs} erreurs rencontrées.")

    def dechiffrer_dossier(self):
        if not self.chemin_cible:
            QMessageBox.warning(self, "Erreur", "Veuillez d'abord choisir un dossier.")
            return

        # Sécurité : on désactive les boutons pendant le travail
        self.btn_chiffrer.setEnabled(False)
        self.btn_dechiffrer.setEnabled(False)
        self.btn_choisir.setEnabled(False)
        QApplication.processEvents()

        fichiers_traites = 0
        erreurs = 0

        for racine, sous_dossiers, fichiers in os.walk(self.chemin_cible):
            for nom_fichier in fichiers:
                if not nom_fichier.endswith(".enc"):
                    continue
                    
                chemin_complet = os.path.join(racine, nom_fichier)
                chemin_original = chemin_complet[:-4]
                
                try:
                    with open(chemin_complet, "rb") as f_in, open(chemin_original, "wb") as f_out:
                        nonce = f_in.read(16)
                        cipher = Cipher(algorithms.ChaCha20(self.cle, nonce), mode=None)
                        decryptor = cipher.decryptor()
                        
                        while True:
                            chunk = f_in.read(self.taille_chunk)
                            if not chunk:
                                break
                            f_out.write(decryptor.update(chunk))
                            
                    os.remove(chemin_complet)
                    fichiers_traites += 1
                    QApplication.processEvents()
                    
                except Exception as e:
                    erreurs += 1
                    print(f"Erreur de déchiffrement sur {nom_fichier} : {e}")

        # On réactive les boutons
        self.btn_chiffrer.setEnabled(True)
        self.btn_dechiffrer.setEnabled(True)
        self.btn_choisir.setEnabled(True)

        QMessageBox.information(self, "Terminé", f"{fichiers_traites} fichiers déchiffrés.\n{erreurs} erreurs rencontrées.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = LogicielCryptage()
    fenetre.show()
    sys.exit(app.exec())
    
    
    