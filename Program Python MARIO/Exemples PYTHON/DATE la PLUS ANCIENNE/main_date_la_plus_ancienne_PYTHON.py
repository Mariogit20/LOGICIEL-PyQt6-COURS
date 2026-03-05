
# Online Python - IDE, Editor, Compiler, Interpreter

# ✅ 1) Fonction collect_dates() – filtre les dates au format YYYY-MM-DD HH:MM
import re

def collect_dates(donnees):
    # Filtrer les dates qui correspondent exactement au format 'YYYY-MM-DD HH:MM'
    pattern = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$'
    tab_date_debut = [date for date in donnees if re.match(pattern, date)]
    return tab_date_debut

# ✅ 2) Fonction get_minimum_date() – retourne uniquement la date sans l'heure (YYYY-MM-DD)
from datetime import datetime

def get_minimum_date(tab_date_debut):
    if not tab_date_debut:
        return None

    # Convertir les chaînes en objets datetime pour comparaison
    dates_obj = [datetime.strptime(date_str, '%Y-%m-%d %H:%M') for date_str in tab_date_debut]
    
    # Trouver la date la plus ancienne
    min_date = min(dates_obj)
    
    # Retourner la partie date seulement (sans l'heure)
    return min_date.strftime('%Y-%m-%d')

# 🧪 Exemple d’utilisation :
donnees = []
i = 0
while i < 4:
    if i == 0:
        donnees.append('2025-11-14 13:27')
    elif i == 1:
        donnees.append('2025-10-12 09:15')
    elif i == 2:
        donnees.append('2025-10-12 17:30')
    elif i == 3:
        donnees.append('2025-11-10 08:45')
    i += 1

tab_date_debut = collect_dates(donnees)
date_min = get_minimum_date(tab_date_debut)

print("Date la plus ancienne (sans l'heure) :", date_min)

# ✅ Résultat attendu :
# Date la plus ancienne (sans l'heure) : 2025-10-12