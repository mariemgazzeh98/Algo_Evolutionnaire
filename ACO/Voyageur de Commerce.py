import numpy as np

# Distances entre 4 ville
dist = np.array([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]])
n_villes = 4
pheromone = np.ones((n_villes, n_villes)) 
taux = 0.5 # Taux d'évaporation

def run_aco_tsp():
    global pheromone
    best_dist = float('inf')
    
    for _ in range(10): # Iterations
        chemin = [0] 
        current = 0
        villes_libres = [1, 2, 3]
        
        while villes_libres:
            
            probs = []
            for v in villes_libres:
                p = (pheromone[current, v]**1) * ((1.0/dist[current, v])**2)
                probs.append(p)
            
            probs = np.array(probs) / sum(probs)
            next_v = np.random.choice(villes_libres, p=probs)
            chemin.append(next_v)
            villes_libres.remove(next_v)
            current = next_v
        
        # Calcul distance 
        d_totale = sum(dist[chemin[i], chemin[i+1]] for i in range(len(chemin)-1)) + dist[chemin[-1], chemin[0]]
        if d_totale < best_dist: best_dist = d_totale
        
        # Evaporation 
        pheromone *= (1 - taux)
        for i in range(len(chemin)-1):
            pheromone[chemin[i], chemin[i+1]] += 1.0/d_totale

    return best_dist

print(f"meuilleur distance: {run_aco_tsp()}")