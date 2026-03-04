# 1. Définition de la classe (le modèle)
class Voiture:
    def __init__(self, marque, couleur):
        self.marque = marque
        self.couleur = couleur

# 2. Création d'instances (les objets concrets)
voiture_1 = Voiture("Peugeot", "Rouge")
voiture_2 = Voiture("Renault", "Bleu")

print(f"Marque de la Voiture 1 = {voiture_1.marque}")

print(f"Couleur de la Voiture 1 = {voiture_1.couleur}")


