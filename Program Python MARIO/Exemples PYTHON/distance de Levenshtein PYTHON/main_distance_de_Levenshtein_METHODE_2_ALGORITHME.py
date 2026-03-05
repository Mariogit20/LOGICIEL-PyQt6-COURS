
# DEFINITION de la distance de Levenshtein, ou distance d'édition :

# La distance de Levenshtein, ou distance d'édition, est une mesure de la similarité entre deux chaînes de caractères. Elle est égale au nombre minimal de modifications (insertions, suppressions ou substitutions) de caractères nécessaires pour transformer une chaîne en une autre.

# Voici deux manières de la calculer en Python :
# 1. Utilisation de la bibliothèque python-Levenshtein

# C'est la méthode la plus simple et la plus performante, car elle est implémentée en C

# 2. Implémentation manuelle (approche par programmation dynamique)

# Cette approche est utile pour comprendre le fonctionnement de l'algorithme. Elle utilise une matrice pour calculer les distances entre les préfixes des deux chaînes.

# Calcule la distance de Levenshtein entre deux chaînes de caractères.

# On décide dans cet exemple d'UTILISER LA METHODE 2 :

# Calcule la distance de Levenshtein entre deux chaînes de caractères.

# 2. Implémentation manuelle (approche par programmation dynamique)

# EXEMPLES :

# La distance de Levenshtein entre 'niche' et 'chien' est : 4
# La distance de Levenshtein entre 'intention' et 'execution' est : 5

def distance_levenshtein(chaine1, chaine2):
    """
    Calcule la distance de Levenshtein entre deux chaînes de caractères.
    """
    # Récupérer les longueurs des deux chaînes
    longueur1, longueur2 = len(chaine1), len(chaine2)

    # Initialiser une matrice pour stocker les distances
    # La taille est (longueur1 + 1) x (longueur2 + 1)
    dp = [[0] * (longueur2 + 1) for _ in range(longueur1 + 1)]

    # Remplir la première ligne et la première colonne de la matrice
    for i in range(longueur1 + 1):
        dp[i][0] = i
    for j in range(longueur2 + 1):
        dp[0][j] = j

    # Parcourir la matrice pour calculer les distances
    for i in range(1, longueur1 + 1):
        for j in range(1, longueur2 + 1):
            # Le coût de substitution est 0 si les caractères sont identiques, 1 sinon
            cout_substitution = 0 if chaine1[i - 1] == chaine2[j - 1] else 1

            # Calculer le minimum des trois opérations possibles :
            # 1. Insertion (dp[i][j-1] + 1)
            # 2. Suppression (dp[i-1][j] + 1)
            # 3. Substitution (dp[i-1][j-1] + cout_substitution)
            dp[i][j] = min(dp[i - 1][j] + 1,                      # Suppression
                           dp[i][j - 1] + 1,                      # Insertion
                           dp[i - 1][j - 1] + cout_substitution)  # Substitution

    # La distance finale se trouve dans la dernière cellule de la matrice
    return dp[longueur1][longueur2]

# Exemple d'utilisation
chaine1 = "niche"
chaine2 = "chien"

dist = distance_levenshtein(chaine1, chaine2)
print(f"La distance de Levenshtein entre '{chaine1}' et '{chaine2}' est : {dist}")  # La distance de Levenshtein entre 'niche' et 'chien' est : 4

chaine3 = "intention"
chaine4 = "execution"

dist2 = distance_levenshtein(chaine3, chaine4)
print(f"La distance de Levenshtein entre '{chaine3}' et '{chaine4}' est : {dist2}") # La distance de Levenshtein entre 'intention' et 'execution' est : 5