"""
# https://www.maxicours.com/se/cours/rechercher-et-inserer-une-cle-dans-un-arbre-binaire-de-recherche/

# https://www.maxicours.com/se/cours/rechercher-et-inserer-une-cle-dans-un-arbre-binaire-de-recherche/

2. Insérer une clé dans un arbre binaire de recherche 
a. Principe 
L’insertion d’une clé dans un arbre binaire de recherche non vide consiste à parcourir l’arbre comme pour rechercher une clé.

On crée ensuite, avec la clé, un nouveau nœud à l’endroit où la recherche s’est arrêtée. 




Voici la fonction précédente testée avec cet arbre sur Python Tutor.

Python 3.6
"""


class ArbreBinaire:
    def __init__(self, etiquette = None, sag = None, sad = None):
        self.etiquette = etiquette
        self.sag = sag
        self.sad = sad
    
    def est_vide(self):
        if self.etiquette is None:
               return True
        else:
               return False 

# Définition de l'arbre :
#         7
#      /     \
#     4       9
#    / \     / \
#   2   5   8   10
#  / \
# 1   3

a = ArbreBinaire()
a.etiquette = 7
a.sag = ArbreBinaire(4)
a.sad = ArbreBinaire(9)
a.sag.sag = ArbreBinaire(2)
a.sag.sad = ArbreBinaire(5, ArbreBinaire(), ArbreBinaire())
a.sad.sag = ArbreBinaire(8, ArbreBinaire(), ArbreBinaire())
a.sad.sad = ArbreBinaire(10, ArbreBinaire(), ArbreBinaire())
a.sag.sag.sag = ArbreBinaire(1, ArbreBinaire(), ArbreBinaire())
a.sag.sag.sad = ArbreBinaire(3, ArbreBinaire(), ArbreBinaire())

 

def insertion(arbre, cle):
    if arbre.est_vide():
        arbre.etiquette = cle
        return "Fait !"
    else:
        if arbre.etiquette < cle:
            if arbre.sad.est_vide():
                arbre.sad.etiquette = cle
                return "Fait !"
            else:
                return insertion(arbre.sad, cle)
        elif arbre.etiquette > cle:
            if arbre.sag.est_vide():
                arbre.sag.etiquette = cle
                return "Fait !"
            else:
                return insertion(arbre.sag, cle)
        else:
            return "Cette clé est déjà présente dans l'arbre."


print("Insertion de 6 : ", insertion(a, 6))
print("Vérification de la présence de 6 : ", a.sag.sad.sad.etiquette == 6)
"""	
a.sag.sad.sad.etiquette renvoie 6. La clé 6 a bien été insérée.
"""