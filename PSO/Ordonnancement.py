import numpy as np

# Tasks processing times
tasks_times = [10, 5, 8, 12] 

def calculate_makespan(sequence):
    
    return sum(tasks_times[i] for i in sequence)

n_particles = 5
dim = len(tasks_times)
X = np.random.rand(n_particles, dim) # nombres entre 0 et 1
V = np.zeros((n_particles, dim))
pbest = X.copy()

def get_sequence(x_row):
    # SPV Rule
    return np.argsort(x_row)

for _ in range(30):
    for i in range(n_particles):
        V[i] = 0.5*V[i] + 2*np.random.rand()*(pbest[i]-X[i])
        X[i] = X[i] + V[i]
        
        current_seq = get_sequence(X[i])
        pbest_seq = get_sequence(pbest[i])
        
        
        if calculate_makespan(current_seq) < calculate_makespan(pbest_seq):
            pbest[i] = X[i].copy()

best_idx = np.argmin([calculate_makespan(get_sequence(p)) for p in pbest])
gbest_seq = get_sequence(pbest[best_idx])
print(f"chemin: {gbest_seq} | Makespan: {calculate_makespan(gbest_seq)}")