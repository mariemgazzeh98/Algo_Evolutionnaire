import random

# --------------------------------------------------------------------------
# --- C'est le code ORIGINAL, sans changement dans les fonctions ---
# --------------------------------------------------------------------------

def calculer_cout(individu):
    """Calcule le coût total de complétion."""
    temps_completion = 0
    temps_actuel = 0
    for tache in individu:
        temps_actuel += tache['duree']
        temps_completion += temps_actuel
    return temps_completion

def calculer_fitness(individu):
    """La fitness est l'inverse du coût."""
    cout = calculer_cout(individu)
    return 1 / cout if cout != 0 else 0

# ... Toutes les autres fonctions (creer_population, selection, croisement, mutation)
# sont exactement les mêmes que dans les codes précédents.
# Je les remets ici pour que le code soit complet.

def creer_population_initiale(taches, taille_population):
    population = []
    for _ in range(taille_population):
        individu = taches[:]
        random.shuffle(individu)
        population.append(individu)
    return population

def selection_roulette(population, fitnesses):
    total_fitness = sum(fitnesses)
    if total_fitness == 0: return random.sample(population, 2)
    selection_probs = [f / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents[0], parents[1]

def selection_par_rang(population, fitnesses):
    population_triee = [x for _, x in sorted(zip(fitnesses, population), key=lambda pair: pair[0], reverse=True)]
    rangs = list(range(len(population_triee), 0, -1))
    total_rangs = sum(rangs)
    selection_probs = [r / total_rangs for r in rangs]
    parents = random.choices(population_triee, weights=selection_probs, k=2)
    return parents[0], parents[1]

def croisement_simple(parent1, parent2):
    point_coupure = random.randint(1, len(parent1) - 1)
    enfant1 = parent1[:point_coupure]
    enfant1.extend([gene for gene in parent2 if gene not in enfant1])
    enfant2 = parent2[:point_coupure]
    enfant2.extend([gene for gene in parent1 if gene not in enfant2])
    return enfant1, enfant2

def croisement_double(parent1, parent2):
    size = len(parent1)
    enfant1 = [None] * size
    p1, p2 = sorted(random.sample(range(size), 2))
    enfant1[p1:p2] = parent1[p1:p2]
    genes_parent2 = [item for item in parent2 if item not in enfant1]
    ptr = 0
    for i in range(size):
        if enfant1[i] is None:
            enfant1[i] = genes_parent2[ptr]
            ptr += 1
    enfant2, _ = croisement_simple(parent2, parent1)
    return enfant1, enfant2

def croisement_uniforme(parent1, parent2):
    size = len(parent1)
    enfant1 = [None] * size
    for i in range(size):
        if random.random() < 0.5:
            if parent1[i] not in enfant1:
                enfant1[i] = parent1[i]
    genes_parent2 = [item for item in parent2 if item not in enfant1]
    for i in range(size):
        if enfant1[i] is None:
            enfant1[i] = genes_parent2.pop(0)
    enfant2, _ = croisement_simple(parent2, parent1)
    return enfant1, enfant2

def mutation(individu, taux_mutation):
    if random.random() < taux_mutation:
        i, j = random.sample(range(len(individu)), 2)
        individu[i], individu[j] = individu[j], individu[i]
    return individu

def algorithme_genetique(taches, taille_population, generations, taux_mutation, methode_selection, methode_croisement):
    population = creer_population_initiale(taches, taille_population)
    for _ in range(generations):
        fitnesses = [calculer_fitness(ind) for ind in population]
        nouvelle_population = []
        for _ in range(taille_population // 2):
            if methode_selection == 'roulette':
                parent1, parent2 = selection_roulette(population, fitnesses)
            else:
                parent1, parent2 = selection_par_rang(population, fitnesses)
            if methode_croisement == 'simple':
                enfant1, enfant2 = croisement_simple(parent1, parent2)
            elif methode_croisement == 'double':
                enfant1, enfant2 = croisement_double(parent1, parent2)
            else:
                enfant1, enfant2 = croisement_uniforme(parent1, parent2)
            nouvelle_population.append(mutation(enfant1, taux_mutation))
            nouvelle_population.append(mutation(enfant2, taux_mutation))
        population = nouvelle_population
    meilleur_individu = max(population, key=calculer_fitness)
    meilleur_cout = calculer_cout(meilleur_individu)
    return meilleur_individu, meilleur_cout

# --------------------------------------------------------------------------
# --- Bloc d'Exécution avec les NOUVEAUX PARAMÈTRES ---
# --------------------------------------------------------------------------

taches_originales = [
    {'id': 'T1', 'duree': 5}, {'id': 'T2', 'duree': 3}, {'id': 'T3', 'duree': 8},
    {'id': 'T4', 'duree': 2}, {'id': 'T5', 'duree': 6}
]

methodes_selection = ['roulette', 'rang']
methodes_croisement = ['simple', 'double', 'uniforme']
titres_croisement = {'simple': "Croisement Simple", 'double': "Croisement Double", 'uniforme': "Croisement Uniforme"}

for sel_methode in methodes_selection:
    print(f"Lancement de l'algorithme génétique avec SÉLECTION PAR {sel_methode.upper()}...")
    print("-" * 55)

    for cross_methode in methodes_croisement:
        solution_optimale, cout_minimal = algorithme_genetique(
            taches=taches_originales,
            # --- PARAMÈTRES MODIFIÉS ICI ---
            taille_population=10,  # Très petite population
            generations=5,       # Très peu de générations
            taux_mutation=0.5,     # Taux de mutation très élevé (50%)
            # -----------------------------
            methode_selection=sel_methode,
            methode_croisement=cross_methode
        )

        solution_ids = [t['id'] for t in solution_optimale]
        
        print(f"--- Résultat avec {titres_croisement[cross_methode]} ---")
        print(f"Solution trouvée: {solution_ids}")
        print(f"Coût: {round(cout_minimal)}")
        print()

    print("\n")