import random
from collections import deque

# --- Définition des fonctions ---

def calculer_distance_totale(solution, matrice_distances):
    """Calcule la distance totale d'un chemin (une solution)."""
    distance_totale = 0
    # Somme des distances entre les villes consécutives
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    # Ajout de la distance entre la dernière et la première ville pour boucler le circuit
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

def generer_voisins(solution):
    """Génère toutes les solutions voisines en échangeant deux villes."""
    voisins = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            voisin = solution[:]  # Crée une copie de la solution actuelle
            # Échange (swap) de deux villes
            voisin[i], voisin[j] = voisin[j], voisin[i]
            voisins.append(voisin)
    return voisins

def tabu_search(matrice_distances, nombre_iterations, taille_tabu):
    """
    Exécute l'algorithme de recherche Tabou pour trouver le chemin le plus court.
    """
    nombre_villes = len(matrice_distances)
    
    # 1. Générer une solution initiale aléatoire
    solution_actuelle = list(range(nombre_villes))
    random.shuffle(solution_actuelle)

    # 2. Initialiser la meilleure solution et la liste tabou
    meilleure_solution = solution_actuelle[:]
    meilleure_distance = calculer_distance_totale(solution_actuelle, matrice_distances)
    
    # La liste tabou stocke les solutions récemment visitées pour éviter les cycles
    tabu_list = deque(maxlen=taille_tabu)

    for _ in range(nombre_iterations):
        # 3. Générer le voisinage de la solution actuelle
        voisinage = generer_voisins(solution_actuelle)
        
        # Filtrer les voisins qui sont dans la liste tabou
        voisins_non_tabous = [v for v in voisinage if tuple(v) not in tabu_list]

        if not voisins_non_tabous:
            # S'il n'y a pas de voisins non tabous, on arrête
            break

        # 4. Sélectionner le meilleur voisin parmi ceux non tabous
        solution_actuelle = min(voisins_non_tabous, key=lambda x: calculer_distance_totale(x, matrice_distances))
        distance_actuelle = calculer_distance_totale(solution_actuelle, matrice_distances)
        
        # 5. Mettre à jour la liste tabou
        tabu_list.append(tuple(solution_actuelle))

        # 6. Mettre à jour la meilleure solution si une meilleure a été trouvée
        if distance_actuelle < meilleure_distance:
            meilleure_solution = solution_actuelle[:]
            meilleure_distance = distance_actuelle

    return meilleure_solution, meilleure_distance

# --- Données du problème et exécution ---

# Matrice des distances (combinée à partir des deux images)
matrice_distances = [
    [0, 2, 7, 15, 2, 5, 7, 6, 5, 2],
    [2, 0, 10, 4, 7, 3, 3, 1, 15, 8],
    [7, 10, 0, 4, 3, 2, 1, 15, 3, 2],
    [15, 4, 4, 0, 15, 7, 7, 2, 5, 4],
    [2, 7, 3, 15, 0, 3, 2, 2, 2, 7],
    [5, 3, 2, 7, 3, 0, 1, 7, 3, 2],
    [7, 3, 1, 7, 2, 1, 0, 7, 3, 2],
    [6, 1, 15, 2, 2, 7, 7, 0, 7, 7],
    [5, 15, 3, 5, 2, 3, 3, 7, 0, 7],
    [2, 8, 2, 4, 7, 2, 2, 7, 7, 0]
]

# Paramètres de l'algorithme
nombre_iterations = 1000
taille_tabu = 50

# Lancement de la recherche
meilleure_solution, meilleure_distance = tabu_search(matrice_distances, nombre_iterations, taille_tabu)

# Affichage des résultats
print(f"Meilleure solution trouvée (Tabu Search): {meilleure_solution}")
print(f"Distance minimale: {meilleure_distance}")