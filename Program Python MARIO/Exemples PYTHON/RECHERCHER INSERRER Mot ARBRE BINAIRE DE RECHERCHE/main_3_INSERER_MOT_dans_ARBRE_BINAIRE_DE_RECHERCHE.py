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
#          a7
#       /      \
#     a4       a9
#     / \       / \
#   a2   a5   a8   a10
#   / \
# a1   a3

a = ArbreBinaire()
a.etiquette = "a7"
a.sag = ArbreBinaire("a4")
a.sad = ArbreBinaire("a9")
a.sag.sag = ArbreBinaire("a2")
a.sag.sad = ArbreBinaire("a5", ArbreBinaire(), ArbreBinaire())
a.sad.sag = ArbreBinaire("a8", ArbreBinaire(), ArbreBinaire())
a.sad.sad = ArbreBinaire("a10", ArbreBinaire(), ArbreBinaire())
a.sag.sag.sag = ArbreBinaire("a1", ArbreBinaire(), ArbreBinaire())
a.sag.sag.sad = ArbreBinaire("a3", ArbreBinaire(), ArbreBinaire())

 

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


print("Insertion de a6 : ", insertion(a, "a6"))
print("Vérification de la présence de a6 : ", a.sag.sad.sad.etiquette == "a6")
"""	
a.sag.sad.sad.etiquette renvoie a6. La clé a6 a bien été insérée.
"""