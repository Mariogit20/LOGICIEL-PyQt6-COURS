from Levenshtein import distance

# DEFINITION de la distance de Levenshtein, ou distance d'édition :

# La distance de Levenshtein, ou distance d'édition, est une mesure de la similarité entre deux chaînes de caractères. Elle est égale au nombre minimal de modifications (insertions, suppressions ou substitutions) de caractères nécessaires pour transformer une chaîne en une autre.

# Voici deux manières de la calculer en Python :
# 1. Utilisation de la bibliothèque python-Levenshtein

# C'est la méthode la plus simple et la plus performante, car elle est implémentée en C

# 2. Implémentation manuelle (approche par programmation dynamique)

# Cette approche est utile pour comprendre le fonctionnement de l'algorithme. Elle utilise une matrice pour calculer les distances entre les préfixes des deux chaînes.

# Calcule la distance de Levenshtein entre deux chaînes de caractères.

# On décide dans cet exemple d'UTILISER LA METHODE 1 :

# 1. Utilisation de la bibliothèque python-Levenshtein

# C'est la méthode la plus simple et la plus performante, car elle est implémentée en C

# Tout d'abord, vous devez installer la bibliothèque via pip :

# pip install python-Levenshtein

# EXEMPLES :

# La distance de Levenshtein entre 'niche' et 'chien' est : 4
# La distance de Levenshtein entre 'intention' et 'execution' est : 5

chaine1 = "niche"
chaine2 = "chien"

dist = distance(chaine1, chaine2)
print(f"La distance de Levenshtein entre '{chaine1}' et '{chaine2}' est : {dist}")  # La distance de Levenshtein entre 'niche' et 'chien' est : 4

chaine3 = "intention"
chaine4 = "execution"

dist2 = distance(chaine3, chaine4)
print(f"La distance de Levenshtein entre '{chaine3}' et '{chaine4}' est : {dist2}")  # La distance de Levenshtein entre 'intention' et 'execution' est : 5