import random
import math

# Matrice des distances (avec la correction sur la 6ème ligne)
matrice_distances = [
    [0, 2, 7, 15, 2, 5, 7, 6, 5, 2],
    [2, 0, 10, 4, 7, 3, 3, 1, 15, 8],
    [7, 10, 0, 4, 3, 2, 1, 15, 3, 2],
    [15, 4, 4, 0, 15, 7, 7, 2, 5, 4],
    [2, 7, 3, 15, 0, 3, 2, 2, 2, 7],
    [5, 3, 2, 7, 3, 0, 1, 7, 3, 2],  # Ligne corrigée (le dernier '2' a été retiré)
    [7, 3, 1, 7, 2, 1, 0, 7, 3, 2],
    [6, 1, 15, 2, 2, 7, 7, 0, 7, 7],
    [5, 15, 3, 5, 2, 3, 3, 7, 0, 7],
    [2, 8, 2, 4, 7, 2, 2, 7, 7, 0]
]

nombre_villes = len(matrice_distances)

# Fonction pour calculer la distance totale d'un chemin (inchangée)
def calculer_distance_totale(solution, matrice_distances):
    distance_totale = 0
    for i in range(len(solution) - 1):
        distance_totale += matrice_distances[solution[i]][solution[i + 1]]
    distance_totale += matrice_distances[solution[-1]][solution[0]]
    return distance_totale

# --- Fonctions pour l'Algorithme Génétique ---

# 1. SELECTION (Roulette) - FONCTION CORRIGÉE
def selection_roulette(population, fitness_scores):
    """
    Sélectionne deux parents en utilisant la méthode de la roulette.
    """
    # Étape 1: Obtenir les indices des deux individus sélectionnés
    indices_selectionnes = random.choices(range(len(population)), weights=fitness_scores, k=2)
    
    # Étape 2: Retourner les deux parents correspondants
    parent1 = population[indices_selectionnes[0]]
    parent2 = population[indices_selectionnes[1]]
    
    return parent1, parent2

# 2. CROISEMENT (fonctions inchangées)
def croisement_simple_ordonne(parent1, parent2):
    size = len(parent1)
    enfant = [None] * size
    point = random.randint(1, size - 2)
    enfant[:point] = parent1[:point]
    pointeur_parent2 = 0
    for i in range(point, size):
        while parent2[pointeur_parent2] in enfant:
            pointeur_parent2 += 1
        enfant[i] = parent2[pointeur_parent2]
    return enfant

def croisement_double_ordonne(parent1, parent2):
    size = len(parent1)
    enfant = [None] * size
    p1, p2 = sorted(random.sample(range(size), 2))
    enfant[p1:p2] = parent1[p1:p2]
    pointeur_parent2 = 0
    for i in list(range(p2, size)) + list(range(p1)):
        while parent2[pointeur_parent2] in enfant:
            pointeur_parent2 += 1
        enfant[i] = parent2[pointeur_parent2]
    return enfant

def croisement_uniforme(parent1, parent2):
    size = len(parent1)
    enfant = [None] * size
    for i in range(size):
        if random.random() < 0.5 and parent1[i] not in enfant:
            enfant[i] = parent1[i]
    for i in range(size):
        if enfant[i] is None:
            for gene in parent2:
                if gene not in enfant:
                    enfant[i] = gene
                    break
    return enfant

# 3. MUTATION (Swap) (inchangée)
def mutation(individu, taux_mutation):
    if random.random() < taux_mutation:
        idx1, idx2 = random.sample(range(len(individu)), 2)
        individu[idx1], individu[idx2] = individu[idx2], individu[idx1]
    return individu

# --- Algorithme Génétique principal --- (inchangé)
def algo_genetique(matrice_distances, taille_population, nb_generations, taux_mutation, methode_croisement):
    population = []
    for _ in range(taille_population):
        individu = list(range(nombre_villes))
        random.shuffle(individu)
        population.append(individu)

    meilleure_solution_globale = None
    meilleure_distance_globale = float('inf')

    for generation in range(nb_generations):
        distances = [calculer_distance_totale(ind, matrice_distances) for ind in population]
        # Vérification pour éviter la division par zéro si une distance est nulle
        fitness_scores = [1 / (d if d > 0 else 1e-9) for d in distances]

        min_distance_gen = min(distances)
        if min_distance_gen < meilleure_distance_globale:
            meilleure_distance_globale = min_distance_gen
            meilleure_solution_globale = population[distances.index(min_distance_gen)]

        nouvelle_population = [meilleure_solution_globale[:]] # Elitisme

        while len(nouvelle_population) < taille_population:
            parent1, parent2 = selection_roulette(population, fitness_scores)
            
            if methode_croisement == 'simple':
                enfant = croisement_simple_ordonne(parent1, parent2)
            elif methode_croisement == 'double':
                enfant = croisement_double_ordonne(parent1, parent2)
            else:
                enfant = croisement_uniforme(parent1, parent2)
            
            enfant = mutation(enfant, taux_mutation)
            nouvelle_population.append(enfant)
            
        population = nouvelle_population
        
    return meilleure_solution_globale, meilleure_distance_globale

# --- Exécution de l'Algorithme Génétique ---
taille_population = 100
nb_generations = 500
taux_mutation = 0.02

print("Lancement de l'algorithme génétique avec SÉLECTION PAR ROULETTE...")
# 1. Avec croisement simple
sol_gen_simple, dist_gen_simple = algo_genetique(matrice_distances, taille_population, nb_generations, taux_mutation, 'simple')
print("\n--- Solution par Algorithme Génétique (Croisement Simple Ordonné) ---")
print(f"Meilleure solution trouvée: {sol_gen_simple}")
print(f"Distance minimale: {dist_gen_simple}")

# 2. Avec croisement double
sol_gen_double, dist_gen_double = algo_genetique(matrice_distances, taille_population, nb_generations, taux_mutation, 'double')
print("\n--- Solution par Algorithme Génétique (Croisement Double Ordonné) ---")
print(f"Meilleure solution trouvée: {sol_gen_double}")
print(f"Distance minimale: {dist_gen_double}")

# 3. Avec croisement uniforme
sol_gen_uniforme, dist_gen_uniforme = algo_genetique(matrice_distances, taille_population, nb_generations, taux_mutation, 'uniforme')
print("\n--- Solution par Algorithme Génétique (Croisement Uniforme) ---")
print(f"Meilleure solution trouvée: {sol_gen_uniforme}")
print(f"Distance minimale: {dist_gen_uniforme}")