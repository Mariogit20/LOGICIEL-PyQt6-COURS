# Visualiseur de Données Interactif (PyQt6 & Matplotlib)

Une application de bureau robuste développée en Python permettant de visualiser, d'exporter et de partager des données statistiques de manière interactive. L'interface graphique sépare complètement sa logique métier de sa source de données (JSON).

## 🚀 Fonctionnalités Principales

* **Interface Graphique Moderne :** Développée avec PyQt6 pour une navigation fluide.
* **Séparation Modèle/Vue :** Les données sont chargées dynamiquement depuis un fichier `JSON` externe, permettant la mise à jour des statistiques sans toucher au code source.
* **Génération de Graphiques :** Création automatique de diagrammes en barres groupées avec Matplotlib (`FigureCanvasQTAgg`).
* **Traçabilité et Exportation :**
  * Export des graphiques en haute résolution (300 DPI) aux formats `.png` et `.jpeg`.
  * Intégration automatique de la date de collecte du JSON et de l'heure de génération sur les images exportées (filigranes).
* **Partage par Email (SMTP) :**
  * Module intégré pour envoyer les rapports (graphiques + JSON) directement depuis le logiciel.
  * Fenêtre de dialogue sécurisée (masquage du mot de passe d'application).
  * Validation stricte des saisies utilisateurs via des expressions régulières (Regex).

## 🛠️ Technologies Utilisées

* **Langage :** Python 3
* **Interface Graphique :** PyQt6
* **Visualisation :** Matplotlib, NumPy
* **Standardisation :** JSON, SMTP, Regex, datetime

## 📦 Installation et Lancement

1. Clonez ce dépôt sur votre machine locale :
   ```bash
   git clone [https://github.com/Mariogit20/nom-de-votre-depot.git](https://github.com/Mariogit20/nom-de-votre-depot.git)
   cd nom-de-votre-depot