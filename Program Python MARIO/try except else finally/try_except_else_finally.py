def diviser_et_enregistrer(numerateur, denominateur_str):
    """
    Tente de diviser un nombre par un autre fourni sous forme de chaîne de caractères,
    puis enregistre le résultat dans un fichier si tout se passe bien.
    """
    fichier = None # Initialisation de la variable pour pouvoir la fermer plus tard
    
    print(f"--- Nouvelle tentative : {numerateur} / '{denominateur_str}' ---")
    
    try:
        # 1. BLOC TRY : Le code "risqué"
        # On met ici uniquement le code susceptible de générer une erreur.
        print("Ouverture du fichier 'journal.txt'...")
        fichier = open("journal.txt", "a") 
        
        print("Conversion du dénominateur en nombre entier...")
        # Risque 1 : ValueError si la chaîne n'est pas un nombre (ex: "chat")
        denominateur = int(denominateur_str) 
        
        print("Calcul de la division...")
        # Risque 2 : ZeroDivisionError si le dénominateur est 0
        resultat = numerateur / denominateur 
        
    except ValueError as erreur_valeur:
        # 2a. BLOC EXCEPT (Spécifique) : Le filet de sécurité pour la conversion
        # Ce bloc s'exécute UNIQUEMENT si une ValueError se produit dans le 'try'.
        print(f"[ERREUR DE SAISIE] Impossible de convertir '{denominateur_str}' en nombre.")
        print(f"   Détail technique : {erreur_valeur}")
        
    except ZeroDivisionError as erreur_zero:
        # 2b. BLOC EXCEPT (Spécifique) : Le filet de sécurité pour les mathématiques
        # Ce bloc s'exécute UNIQUEMENT si une ZeroDivisionError se produit.
        print("[ERREUR MATHÉMATIQUE] Vous ne pouvez pas diviser par zéro !")
        print(f"   Détail technique : {erreur_zero}")
        
    except Exception as erreur_inconnue:
        # 2c. BLOC EXCEPT (Générique) : Le filet de sécurité ultime
        # Il attrape toutes les autres erreurs non prévues (problème de disque plein, etc.).
        # Il doit toujours être placé en dernier.
        print(f"[ERREUR CRITIQUE INATTENDUE] Quelque chose s'est mal passé : {erreur_inconnue}")
        
    else:
        # 3. BLOC ELSE : La récompense en cas de succès
        # Ce bloc s'exécute UNIQUEMENT si le bloc 'try' s'est terminé sans AUCUNE erreur.
        # C'est une bonne pratique de mettre ici le code qui dépend de la réussite du 'try'.
        print(f"[SUCCÈS] Le calcul est terminé. Résultat = {resultat}")
        fichier.write(f"Succès : {numerateur} / {denominateur} = {resultat}\n")
        print("Le résultat a été enregistré dans le fichier journal.")
        
    finally:
        # 4. BLOC FINALLY : Le "nettoyeur" implacable
        # Ce bloc s'exécute TOUJOURS, à 100%, qu'il y ait eu une erreur ou non dans le 'try'.
        # Il est utilisé pour libérer les ressources (fermer un fichier, une base de données...).
        print("Phase de nettoyage...")
        if fichier is not None and not fichier.closed:
            fichier.close()
            print("Le fichier 'journal.txt' a été fermé en toute sécurité.")
        else:
            print("Aucun fichier ouvert à fermer.")
        print("--- Fin de l'opération ---\n")


# ==========================================
# TESTS POUR VOIR LE COMPORTEMENT EN ACTION
# ==========================================

# Test 1 : Tout se passe bien (déclenche try -> else -> finally)
diviser_et_enregistrer(10, "2")

# Test 2 : Erreur mathématique (déclenche try -> except ZeroDivisionError -> finally)
diviser_et_enregistrer(10, "0")

# Test 3 : Erreur de saisie (déclenche try -> except ValueError -> finally)
diviser_et_enregistrer(10, "chat")



