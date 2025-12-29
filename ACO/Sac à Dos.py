import numpy as np

items = [(10, 2), (20, 4), (30, 6), (40, 8)] # (Value, Weight)
cap_max = 10 #capacité maximal
pheromone_items = np.ones(len(items))

for _ in range(20):
    sac = []
    poids_actuel = 0
    indices = list(range(len(items)))
    
    np.random.shuffle(indices) 
    for i in indices:
        # Probabilité 
        h = items[i][0] / items[i][1] # Value/Weight
        prob_take = (pheromone_items[i] * h) / 100 
        
        if np.random.rand() < prob_take and poids_actuel + items[i][1] <= cap_max:
            sac.append(i)
            poids_actuel += items[i][1]
            
    # Update pheromone selon Value
    val_tot = sum(items[i][0] for i in sac)
    for i in sac:
        pheromone_items[i] += val_tot * 0.01

print(f"pheromone de chaque objet de sac: {pheromone_items}")
