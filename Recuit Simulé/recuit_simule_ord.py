import random
import math

def calculer_cout(ordonnancement):
    """Calcule le coût total d'un ordonnancement."""
    temps_completion = 0
    temps_actuel = 0
    for tache in ordonnancement:
        temps_actuel += tache['duree']
        temps_completion += temps_actuel
    return temps_completion

def generer_voisin(ordonnancement):
    """Génère un ordonnancement voisin en permutant deux tâches."""
    voisin = ordonnancement[:]
    i, j = random.sample(range(len(voisin)), 2)
    voisin[i], voisin[j] = voisin[j], voisin[i]
    return voisin

def recuit_simule(taches, temperature_initiale, taux_refroidissement, max_iterations):
    """
    Exécute l'algorithme du recuit simulé pour l'ordonnancement de tâches.
    """
    solution_actuelle = taches[:]
    random.shuffle(solution_actuelle)
    meilleure_solution = solution_actuelle
    meilleur_cout = calculer_cout(solution_actuelle)
    
    temperature = temperature_initiale

    for _ in range(max_iterations):
        voisin = generer_voisin(solution_actuelle)
        cout_actuel = calculer_cout(solution_actuelle)
        cout_voisin = calculer_cout(voisin)
        
        # Si le voisin est meilleur, on l'accepte
        if cout_voisin < cout_actuel:
            solution_actuelle = voisin
            if cout_voisin < meilleur_cout:
                meilleure_solution = voisin
                meilleur_cout = cout_voisin
        # Sinon, on l'accepte avec une certaine probabilité
        else:
            probabilite_acceptation = math.exp((cout_actuel - cout_voisin) / temperature)
            if random.random() < probabilite_acceptation:
                solution_actuelle = voisin
        
        # Refroidissement
        temperature *= taux_refroidissement

    return meilleure_solution, meilleur_cout

# Exemple d'utilisation
taches = [
    {'id': 'T1', 'duree': 5},
    {'id': 'T2', 'duree': 3},
    {'id': 'T3', 'duree': 8},
    {'id': 'T4', 'duree': 2},
    {'id': 'T5', 'duree': 6}
]

solution_optimale_recuit, cout_optimal_recuit = recuit_simule(taches, temperature_initiale=1000, taux_refroidissement=0.99, max_iterations=1000)
print("\nRecuit Simulé - Meilleur ordonnancement:", [t['id'] for t in solution_optimale_recuit])
print("Recuit Simulé - Coût optimal:", cout_optimal_recuit)