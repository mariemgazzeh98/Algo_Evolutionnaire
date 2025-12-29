import numpy as np

# Items: (Valeur, Poids)
items = [(10, 2), (20, 4), (30, 6), (40, 8)]
cap_max = 10

def fitness(position):
    val_tot = 0
    poids_tot = 0
    for i in range(len(position)):
        if position[i] == 1:
            val_tot += items[i][0]
            poids_tot += items[i][1]
    if poids_tot > cap_max: return 0 # Penalty
    return val_tot

def sigmoid(v):
    return 1 / (1 + np.exp(-v))

n_particles = 10
dim = len(items)
X = np.random.randint(2, size=(n_particles, dim)) # Positions 0 ou 1
V = np.zeros((n_particles, dim)) # Vitesses
pbest = X.copy()
gbest = X[0]

for _ in range(50):
    for i in range(n_particles):
        # Update Vitesse
        V[i] = 0.5*V[i] + 1.5*np.random.rand()*(pbest[i]-X[i]) + 1.5*np.random.rand()*(gbest-X[i])
        
        # Update Position (Sigmoid logic)
        for d in range(dim):
            if np.random.rand() < sigmoid(V[i, d]):
                X[i, d] = 1
            else:
                X[i, d] = 0
        
        # Update pbests
        if fitness(X[i]) > fitness(pbest[i]): pbest[i] = X[i].copy()
        if fitness(pbest[i]) > fitness(gbest): gbest = pbest[i].copy()

print(f"maeuilleur Selection: {gbest}  Valeur: {fitness(gbest)}")