import random
import math

# Matrice des distances fournie dans l'image
matrice_distances = [
    [0, 2, 7, 15, 2, 5, 7, 6, 5, 2],
    [2, 0, 10, 4, 7, 3, 3, 1, 15, 8],
    [7, 10, 0, 4, 3, 2, 1, 15, 3, 2],
    [15, 4, 4, 0, 15, 7, 7, 2, 5, 4],
    [2, 7, 3, 15, 0, 3, 2, 2, 2, 7],
    [5, 3, 2, 7, 3, 0, 1, 7, 3, 2, 2],
    [7, 3, 1, 7, 2, 1, 0, 7, 3, 2],
    [6, 1, 15, 2, 2, 7, 7, 0, 7, 7],
    [5, 15, 3, 5, 2, 3, 3, 7, 0, 7],
    [2, 8, 2, 4, 7, 2, 2, 7, 7, 0]
]

nombre_villes = len(matrice_distances)

# Fonction pour calculer la distance totale d'un chemin (réutilisée)
def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    # Ajouter la distance pour revenir à la ville de départ
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale
def recuit_simule(matrice_distances, temp_initiale, taux_refroidissement, nombre_iterations):
    """
    Résout le problème du voyageur de commerce en utilisant le recuit simulé.
    """
    # 1. Générer une solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)
    distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)

    meilleure_solution = solution_actuelle[:]
    meilleure_distance = distance_actuelle

    temperature = temp_initiale

    for i in range(nombre_iterations):
        # 2. Générer un voisin en inversant un segment du chemin (2-opt)
        voisin = solution_actuelle[:]
        l, r = sorted(random.sample(range(nombre_villes), 2))
        voisin[l:r+1] = reversed(voisin[l:r+1])
        
        distance_voisin = calculer_distance_totale(voisin, matrice_distances)

        # 3. Décider d'accepter ou non la nouvelle solution
        diff_distance = distance_voisin - distance_actuelle

        if diff_distance < 0 or random.random() < math.exp(-diff_distance / temperature):
            solution_actuelle = voisin[:]
            distance_actuelle = distance_voisin

        # Mettre à jour la meilleure solution trouvée
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle
            
        # 4. Refroidir la température
        temperature *= taux_refroidissement

    return meilleure_solution, meilleure_distance

# --- Exécution du Recuit Simulé ---
temp_initiale = 1000
taux_refroidissement = 0.995
nombre_iterations_recuit = 10000

meilleure_solution_recuit, meilleure_distance_recuit = recuit_simule(
    matrice_distances, temp_initiale, taux_refroidissement, nombre_iterations_recuit
)

print("\n--- Solution par Recuit Simulé ---")
print(f"Meilleure solution trouvée: {meilleure_solution_recuit}")
print(f"Distance minimale: {meilleure_distance_recuit}")