import sys
import json
import os
import smtplib
import re
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QComboBox, QLabel, QHBoxLayout, QMessageBox, 
                             QPushButton, QFileDialog, QDialog, QFormLayout, 
                             QLineEdit, QDialogButtonBox)
from PyQt6.QtGui import QIcon 

# =====================================================================
# FONCTION POUR GÉRER LES CHEMINS (COMPATIBLE PYINSTALLER)
# =====================================================================
def resource_path(relative_path):
    """ Obtenir le chemin absolu vers la ressource, fonctionne pour le dev et pour PyInstaller """
    try:
        # PyInstaller crée un dossier temporaire et stocke le chemin dans _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# =====================================================================
# CLASSE : FENÊTRE DE DIALOGUE POUR L'EMAIL
# =====================================================================
class DialogueEmail(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration de l'Email")
        self.setMinimumWidth(400)

        # --- AJOUT DE L'ICÔNE SUR LA FENÊTRE DE DIALOGUE ---
        chemin_icone = resource_path("app_icon.png")
        self.setWindowIcon(QIcon(chemin_icone))
        # ---------------------------------------------------

        layout = QFormLayout(self)

        self.champ_expediteur = QLineEdit(self)
        self.champ_expediteur.setPlaceholderText("votre.email@gmail.com")

        self.champ_mdp = QLineEdit(self)
        self.champ_mdp.setEchoMode(QLineEdit.EchoMode.Password)
        self.champ_mdp.setPlaceholderText("Mot de passe d'application (16 lettres)")

        self.champ_destinataire = QLineEdit(self)
        self.champ_destinataire.setPlaceholderText("destinataire@exemple.com")

        layout.addRow("Votre email Gmail :", self.champ_expediteur)
        layout.addRow("Mot de passe d'app :", self.champ_mdp)
        layout.addRow("Email destinataire :", self.champ_destinataire)

        boutons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        boutons.accepted.connect(self.accept)
        boutons.rejected.connect(self.reject)
        layout.addWidget(boutons)

    def obtenir_donnees(self):
        return self.champ_expediteur.text(), self.champ_mdp.text(), self.champ_destinataire.text()

# =====================================================================
# CLASSE PRINCIPALE : L'APPLICATION
# =====================================================================
class FenetrePrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Base de données Animale depuis JSON")
        self.setGeometry(100, 100, 1000, 650)

        # --- AJOUT DE L'ICÔNE SUR LA FENÊTRE PRINCIPALE ---
        chemin_icone = resource_path("app_icon.png")
        self.setWindowIcon(QIcon(chemin_icone))
        # --------------------------------------------------

        # --- 1. CHARGEMENT DES DONNÉES ---
        donnees_completes = self.charger_donnees_json("matplotlib_gemini3_1_pro5.json")
        
        if not donnees_completes:
            return

        # Extraction de la date de collecte du JSON
        metadata = donnees_completes.pop("_Metadata", {})
        self.date_collecte_json = metadata.get("date_collecte", "Date non spécifiée")
        self.base_animaux = donnees_completes

        # --- 2. INTERFACE GRAPHIQUE ---
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        layout_principal = QVBoxLayout(widget_central)

        # Étiquette de la date de collecte en haut
        label_date_collecte = QLabel(f"📅 Fichier de données collecté le : {self.date_collecte_json}")
        label_date_collecte.setStyleSheet("color: #666666; font-style: italic; font-size: 10pt; margin-bottom: 5px;")
        layout_principal.addWidget(label_date_collecte)

        # Menu et Boutons
        layout_menu = QHBoxLayout()
        
        label_menu = QLabel("Choisissez une espèce :")
        self.menu_deroulant = QComboBox()
        self.menu_deroulant.addItems(self.base_animaux.keys())
        self.menu_deroulant.currentTextChanged.connect(self.changer_animal)

        self.btn_export_jpeg = QPushButton("Export JPEG")
        self.btn_export_png = QPushButton("Export PNG")
        self.btn_envoyer_email = QPushButton("📧 Envoyer par Email")
        
        self.btn_export_jpeg.clicked.connect(lambda: self.exporter_image("jpeg"))
        self.btn_export_png.clicked.connect(lambda: self.exporter_image("png"))
        self.btn_envoyer_email.clicked.connect(self.preparer_email)

        layout_menu.addWidget(label_menu)
        layout_menu.addWidget(self.menu_deroulant)
        layout_menu.addStretch()
        layout_menu.addWidget(self.btn_export_jpeg)
        layout_menu.addWidget(self.btn_export_png)
        layout_menu.addWidget(self.btn_envoyer_email)
        
        layout_principal.addLayout(layout_menu)

        # Zone Graphique Matplotlib
        fig, self.ax = plt.subplots(layout='constrained')
        self.canvas = FigureCanvas(fig)
        layout_principal.addWidget(self.canvas)

        self.changer_animal(self.menu_deroulant.currentText())

    # --- 3. GESTION DU JSON ---
    def charger_donnees_json(self, chemin_fichier):
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                donnees_brutes = json.load(fichier)
                donnees_valides, liste_erreurs = self.valider_structure(donnees_brutes)
                if liste_erreurs:
                    message = "Certaines données ont été ignorées :\n\n" + "\n".join(liste_erreurs)
                    QMessageBox.warning(self, "Avertissement", message)
                return donnees_valides
        except FileNotFoundError:
            QMessageBox.critical(self, "Erreur", f"Le fichier {chemin_fichier} est introuvable.")
            return {}
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Erreur", "Le fichier contient des erreurs de syntaxe JSON.")
            return {}
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de lecture du fichier : {e}")
            return {}

    def valider_structure(self, donnees):
        cles_requises = ["categories", "donnees", "unites"]
        donnees_valides = {}
        erreurs = []
        for cle, contenu in donnees.items():
            if cle == "_Metadata":
                donnees_valides[cle] = contenu
                continue
            if not isinstance(contenu, dict):
                continue
            cles_manquantes = [c for c in cles_requises if c not in contenu]
            if cles_manquantes:
                erreurs.append(f"- '{cle}' : clés manquantes ({', '.join(cles_manquantes)})")
            else:
                donnees_valides[cle] = contenu
        return donnees_valides, erreurs

    # --- 4. DESSIN DU GRAPHIQUE ---
    def changer_animal(self, nom_espece):
        if nom_espece in self.base_animaux:
            infos = self.base_animaux[nom_espece]
            self.dessiner_graphique(f"Comparaison des {nom_espece}", infos["categories"], infos["donnees"], infos["unites"])

    def dessiner_graphique(self, titre, categories, donnees, unites):
        self.ax.clear()
        x = np.arange(len(categories))
        width = 0.25
        multiplier = 0
        for attribute, measurement in donnees.items():
            offset = width * multiplier
            rects = self.ax.bar(x + offset, measurement, width, label=attribute)
            unite = unites.get(attribute, "")
            etiquettes = [f"{val} {unite}" for val in measurement]
            self.ax.bar_label(rects, labels=etiquettes, padding=3, fontsize=9)
            multiplier += 1

        self.ax.set_title(titre)
        if len(donnees) > 0:
            self.ax.set_xticks(x + (width * (len(donnees) - 1) / 2), categories)
        self.ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        try:
            max_val = max([max(v) for v in donnees.values() if v])
            self.ax.set_ylim(0, max_val + (max_val * 0.25))
        except ValueError:
            pass
        self.canvas.draw()

    # --- 5. EXPORTATION D'IMAGE ---
    def exporter_image(self, format_image):
        animal_actuel = self.menu_deroulant.currentText()
        maintenant = datetime.now()
        date_heure_fichier = maintenant.strftime("%Y-%m-%d_%Hh%Mm%Ss")
        date_heure_texte = maintenant.strftime("%d/%m/%Y à %H:%M:%S")
        nom_fichier_defaut = f"Graphique_{animal_actuel}_{date_heure_fichier}.{format_image}"
        
        filtre = "Images PNG (*.png)" if format_image == "png" else "Images JPEG (*.jpg *.jpeg)"
        chemin_sauvegarde, _ = QFileDialog.getSaveFileName(self, f"Sauvegarder en {format_image.upper()}", nom_fichier_defaut, filtre)

        if chemin_sauvegarde:
            try:
                # Ajout des dates sur l'image
                texte_collecte = self.ax.figure.text(0.01, 0.99, f"Fichier de données collecté le : {self.date_collecte_json}", 
                                                      ha='left', va='top', fontsize=8, color='#888888', fontstyle='italic')
                texte_generation = self.ax.figure.text(0.99, 0.01, f"Image générée le {date_heure_texte}", 
                                                       ha='right', va='bottom', fontsize=8, color='#888888')
                
                self.ax.figure.savefig(chemin_sauvegarde, format=format_image, dpi=300, bbox_inches='tight')
                
                # Suppression des textes sur l'interface logicielle
                texte_collecte.remove()
                texte_generation.remove()
                self.canvas.draw()
                QMessageBox.information(self, "Succès", f"Graphique exporté avec succès sous :\n{chemin_sauvegarde}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de l'exportation :\n{e}")

    # --- 6. GESTION DE L'EMAIL ---
    def preparer_email(self):
        dialogue = DialogueEmail(self)
        
        if dialogue.exec() == QDialog.DialogCode.Accepted:
            expediteur, mdp, destinataire = dialogue.obtenir_donnees()
            
            # --- VÉRIFICATIONS PAR REGEX ---
            regex_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            
            if not re.match(regex_email, expediteur):
                QMessageBox.warning(self, "Erreur de saisie", "Votre adresse email d'expédition n'a pas un format valide.")
                return 
                
            if not re.match(regex_email, destinataire):
                QMessageBox.warning(self, "Erreur de saisie", "L'adresse email du destinataire n'a pas un format valide.")
                return
                
            # Nettoyage des espaces pour le mot de passe d'application
            mdp_propre = mdp.replace(" ", "") 
            regex_mdp = r'^[a-zA-Z]{16}$' 
            
            if not re.match(regex_mdp, mdp_propre):
                QMessageBox.warning(self, "Erreur de saisie", "Le mot de passe d'application doit contenir exactement 16 lettres (les espaces sont tolérés, mais pas les chiffres).")
                return
            # --- FIN DES VÉRIFICATIONS ---

            chemins_fichiers, _ = QFileDialog.getOpenFileNames(
                self, 
                "Sélectionnez les fichiers à envoyer", 
                "", 
                "Fichiers (*.json *.png *.jpg *.jpeg)"
            )

            if chemins_fichiers:
                self.setWindowTitle("Base de données Animale - Envoi de l'email en cours...")
                QApplication.processEvents()
                
                self.envoyer_email(expediteur, mdp_propre, destinataire, chemins_fichiers)
                
                self.setWindowTitle("Base de données Animale depuis JSON")

    def envoyer_email(self, expediteur, mdp, destinataire, chemins_fichiers):
        sujet = "Graphiques et Données JSON exportés"
        corps = "Bonjour,\n\nVeuillez trouver ci-joint les graphiques ainsi que le fichier de données JSON.\n\nCordialement,\nVotre Logiciel PyQt6"
        
        msg = MIMEMultipart()
        msg['From'] = expediteur
        msg['To'] = destinataire
        msg['Subject'] = sujet
        msg.attach(MIMEText(corps, 'plain'))

        for chemin in chemins_fichiers:
            try:
                with open(chemin, "rb") as fichier:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(fichier.read())
                encoders.encode_base64(part)
                nom_fichier = os.path.basename(chemin)
                
                # --- CORRECTION DE L'ENCODAGE UTF-8 POUR LES ACCENTS ---
                part.add_header("Content-Disposition", "attachment", filename=("utf-8", "", nom_fichier))
                
                msg.attach(part)
            except Exception as e:
                QMessageBox.warning(self, "Avertissement", f"Impossible d'attacher le fichier {chemin}.\nErreur: {e}")

        try:
            serveur = smtplib.SMTP('smtp.gmail.com', 587)
            serveur.starttls()
            serveur.login(expediteur, mdp)
            serveur.sendmail(expediteur, destinataire, msg.as_string())
            serveur.quit()
            
            QMessageBox.information(self, "Succès", "✅ L'email a été envoyé avec succès avec toutes ses pièces jointes !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur d'envoi", f"❌ Échec de l'envoi de l'email.\n\nVérifiez votre connexion internet, votre mot de passe d'application, ou l'adresse du destinataire.\n\nDétails : {e}")

# =====================================================================
# LANCEMENT DE L'APPLICATION
# =====================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    fenetre.show()
    sys.exit(app.exec())