import numpy as np

tasks_times = [10, 5, 8, 12] 
n_tasks = len(tasks_times)
pheromone = np.ones((n_tasks, n_tasks))

for _ in range(15):
    sequence = []
    available = list(range(n_tasks))
    current = np.random.choice(available) 
    sequence.append(current)
    available.remove(current)
    
    while available:
        
        probs = []
        for nxt in available:
             
            p = pheromone[current, nxt] * (1.0 / tasks_times[nxt])
            probs.append(p)
        
        probs = np.array(probs) / sum(probs)
        next_t = np.random.choice(available, p=probs)
        sequence.append(next_t)
        available.remove(next_t)
        current = next_t

    # Makespan (Total time)
    makespan = sum(tasks_times) 
    # Update pheromone
    for i in range(len(sequence)-1):
        pheromone[sequence[i], sequence[i+1]] += 1.0
        
print(f"meuilleur : {sequence}")