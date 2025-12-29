import numpy as np
import random

# 1. Distance matrice (Exemple 4 villes)
dist_matrix = np.array([
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
])

def calculate_fitness(route):
    distance = 0
    for i in range(len(route)-1):
        distance += dist_matrix[route[i], route[i+1]]
    distance += dist_matrix[route[-1], route[0]] 
    return distance

# PSO TSP
n_villes = 4
n_particles = 10
iterations = 20

# Initialisation
particles = [random.sample(range(n_villes), n_villes) for _ in range(n_particles)]
pbest = list(particles)
gbest = min(pbest, key=lambda x: calculate_fitness(x))

for _ in range(iterations):
    for i in range(n_particles):
        if random.random() < 0.7:
            idx1, idx2 = random.sample(range(n_villes), 2)
            particles[i][idx1], particles[i][idx2] = particles[i][idx2], particles[i][idx1]
        
        # Update pbest
        if calculate_fitness(particles[i]) < calculate_fitness(pbest[i]):
            pbest[i] = list(particles[i])
            
    # Update gbest
    gbest = min(pbest, key=lambda x: calculate_fitness(x))

print(f"meuilleure chemin: {gbest} avec distance: {calculate_fitness(gbest)}")