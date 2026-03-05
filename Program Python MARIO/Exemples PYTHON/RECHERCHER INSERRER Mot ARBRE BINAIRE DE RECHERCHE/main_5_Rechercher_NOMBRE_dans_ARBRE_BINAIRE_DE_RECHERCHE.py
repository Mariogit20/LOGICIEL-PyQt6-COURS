"""
https://www.maxicours.com/se/cours/rechercher-et-inserer-une-cle-dans-un-arbre-binaire-de-recherche/ 
https://www.maxicours.com/se/cours/rechercher-et-inserer-une-cle-dans-un-arbre-binaire-de-recherche/ 

1. Rechercher un NOMBRE dans un arbre binaire de recherche  
a. Principe  La recherche d’une clé dans un arbre binaire de recherche non vide consiste à comparer la clé et la racine, puis, si elles sont différentes, à descendre dans le sous-arbre gauche ou le sous-arbre droit selon que la clé est plus petite ou plus grande que la racine. 
 
La recherche s’arrête quand on trouve la clé dans l’arbre ou quand on a atteint une feuille.  
Si la clé est inférieure à la racine de l’arbre, on recherche dans le sous-arbre gauche.   Si la clé est supérieure à la racine de l’arbre, on recherche dans le sous-arbre droit.  
 

Voici la fonction précédente testée avec cet arbre sur Python Tutor : 
 
 
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





def recherche(arbre, cle): 
 if arbre.est_vide(): 
     return False 
 elif arbre.etiquette == cle: 
     return True 
 else: 
     if arbre.etiquette < cle: 
         return recherche(arbre.sad, cle) 
     else: 
         return recherche(arbre.sag, cle) 




print("Recherche de 8 : ", recherche(a, 8)) 
print("Recherche de 6 : ", recherche(a, 6)) 

# Ces lignes de code permettent de définir la fonction recherche.  
# On pourra ainsi l’utiliser sur l’arbre étudié : print(recherche(a, 8)) renverra True, donc 8 est bien dans l’arbre. Également, print(recherche(a, 6)) renverra False, donc 6 n’est pas dans l’arbre. 



