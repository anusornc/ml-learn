import numpy as np

def run():
    # Let's write a flexible search over 9 points (P1 to P9)
    # P1 = (0.0, 0.1), P2 = (0.1, 0.0), P3 = (0.1, 0.2) -> Min x=0, Min y=0
    # P8 = (0.9, 1.0), P9 = (1.0, 0.9) -> Max x=1, Max y=1
    
    # Let's test a few intuitive layouts
    # Cluster 1: P1=(0.0, 0.1), P2=(0.1, 0.0), P3=(0.2, 0.2)
    # Cluster 2: P4=(0.4, 0.4), P5=(0.5, 0.5), P6=(0.6, 0.4)
    # Cluster 3: P7=(0.8, 0.8), P8=(0.9, 1.0), P9=(1.0, 0.9)
    
    # What if initial centroids are P1, P4, P9?
    # What if P4 is closer to P1 or P5?
    
    # Let's test combinations
    pts = np.array([
        [0.0, 0.1], # P1
        [0.1, 0.0], # P2
        [0.2, 0.2], # P3
        [0.3, 0.4], # P4
        [0.5, 0.5], # P5
        [0.6, 0.4], # P6
        [0.7, 0.7], # P7
        [0.9, 1.0], # P8
        [1.0, 0.9], # P9
    ])
    
    for inits in [(0, 4, 8), (0, 3, 8), (1, 4, 7), (0, 4, 7), (1, 4, 8), (0, 5, 8), (2, 4, 6)]:
        res = simulate(pts, inits)
        print(f"Inits {inits} -> {res}")

def simulate(points, inits):
    centroids = points[list(inits)].copy()
    history = []
    
    for r in range(3):
        dists = np.zeros((len(points), 3))
        for k in range(3):
            dists[:, k] = np.sqrt(np.sum((points - centroids[k])**2, axis=1))
        
        assignments = np.argmin(dists, axis=1) + 1
        counts = [np.sum(assignments == k) for k in [1, 2, 3]]
        
        new_centroids = np.zeros((3, 2))
        for k in range(3):
            if counts[k] == 0:
                return "empty cluster"
            new_centroids[k] = np.mean(points[assignments == (k+1)], axis=0)
            
        dmin = np.min(dists, axis=1)
        wcss = np.sum(dmin**2)
        
        history.append({
            'assignments': assignments.copy(),
            'centroids': centroids.copy(),
            'new_centroids': new_centroids.copy(),
            'wcss': wcss
        })
        centroids = new_centroids.copy()
        
    c1 = np.sum(history[0]['assignments'] != history[1]['assignments'])
    c2 = np.sum(history[1]['assignments'] != history[2]['assignments'])
    return f"c1={c1}, c2={c2}, wcss={[round(h['wcss'], 4) for h in history]}, A1={history[0]['assignments']}, A2={history[1]['assignments']}, A3={history[2]['assignments']}"

run()
