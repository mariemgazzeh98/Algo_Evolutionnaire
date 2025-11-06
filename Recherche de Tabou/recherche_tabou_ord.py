import random

def calculer_cout(ordonnancement):
    """Calcule le coût total d'un ordonnancement (par exemple, le temps total de complétion)."""
    temps_completion = 0
    temps_actuel = 0
    for tache in ordonnancement:
        temps_actuel += tache['duree']
        temps_completion += temps_actuel
    return temps_completion

def generer_voisin_et_mouvement(ordonnancement):
    """Génère un ordonnancement voisin en permutant deux tâches et retourne le voisin ainsi que le mouvement."""
    voisin = ordonnancement[:]
    # Choisir deux indices distincts au hasard
    i, j = random.sample(range(len(voisin)), 2)
    # Permuter les tâches à ces indices
    voisin[i], voisin[j] = voisin[j], voisin[i]
    # Le mouvement est la paire d'indices permutés, triée pour être cohérente (ex: (1, 3) est pareil que (3, 1))
    mouvement = tuple(sorted((i, j)))
    return voisin, mouvement

def recherche_tabou(taches, taille_liste_tabou, max_iterations):
    """
    Exécute l'algorithme de recherche tabou pour l'ordonnancement de tâches. (Version corrigée)
    """
    solution_actuelle = taches[:]
    random.shuffle(solution_actuelle)
    meilleure_solution = list(solution_actuelle)
    meilleur_cout = calculer_cout(solution_actuelle)
    
    liste_tabou = []

    for _ in range(max_iterations):
        meilleur_voisin = None
        meilleur_voisin_cout = float('inf')
        meilleur_mouvement_fait = None

        # Explorer le voisinage
        for _ in range(len(taches) * 2): # Nombre de voisins à explorer à chaque itération
            voisin, mouvement = generer_voisin_et_mouvement(solution_actuelle)
            
            # Vérifier si le mouvement n'est pas dans la liste tabou
            if mouvement not in liste_tabou:
                cout_voisin = calculer_cout(voisin)
                # Garder en mémoire le meilleur voisin non-tabou trouvé
                if cout_voisin < meilleur_voisin_cout:
                    meilleur_voisin = voisin
                    meilleur_voisin_cout = cout_voisin
                    meilleur_mouvement_fait = mouvement
        
        if meilleur_voisin is None:
            # Si aucun voisin non-tabou n'a été trouvé, on peut s'arrêter.
            # (Une implémentation plus avancée pourrait utiliser un critère d'aspiration ici)
            break
            
        # Déplacer vers le meilleur voisin trouvé
        solution_actuelle = meilleur_voisin
        
        # Ajouter le mouvement effectué à la liste tabou
        if meilleur_mouvement_fait is not None:
            liste_tabou.append(meilleur_mouvement_fait)
            if len(liste_tabou) > taille_liste_tabou:
                liste_tabou.pop(0)

        # Mettre à jour la meilleure solution globale si nécessaire
        if meilleur_voisin_cout < meilleur_cout:
            meilleure_solution = meilleur_voisin
            meilleur_cout = meilleur_voisin_cout

    return meilleure_solution, meilleur_cout

# Exemple d'utilisation
taches = [
    {'id': 'T1', 'duree': 5},
    {'id': 'T2', 'duree': 3},
    {'id': 'T3', 'duree': 8},
    {'id': 'T4', 'duree': 2},
    {'id': 'T5', 'duree': 6}
]

solution_optimale_tabou, cout_optimal_tabou = recherche_tabou(taches, taille_liste_tabou=5, max_iterations=100)
print("Recherche Tabou - Meilleur ordonnancement:", [t['id'] for t in solution_optimale_tabou])
print("Recherche Tabou - Coût optimal:", cout_optimal_tabou)