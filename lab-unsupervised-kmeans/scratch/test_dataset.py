import numpy as np

def run_kmeans_sim(data_raw, init_indices, feature_names=["X1", "X2"]):
    ids = [d[0] for d in data_raw]
    x1_raw = np.array([d[1] for d in data_raw], dtype=float)
    x2_raw = np.array([d[2] for d in data_raw], dtype=float)
    
    # Min-Max Normalization
    min_x1, max_x1 = np.min(x1_raw), np.max(x1_raw)
    min_x2, max_x2 = np.min(x2_raw), np.max(x2_raw)
    
    range_x1 = max_x1 - min_x1
    range_x2 = max_x2 - min_x2
    
    x1_norm = (x1_raw - min_x1) / range_x1
    x2_norm = (x2_raw - min_x2) / range_x2
    
    points = np.column_stack([x1_norm, x2_norm])
    
    # Initial Centroids
    centroids = points[init_indices].copy()
    
    print("=== SUMMARY OF DATASET ===")
    print(f"{feature_names[0]}: Min={min_x1}, Max={max_x1}, Range={range_x1}")
    print(f"{feature_names[1]}: Min={min_x2}, Max={max_x2}, Range={range_x2}")
    print("\nNormalized Data:")
    for i in range(len(ids)):
        print(f"{ids[i]}: raw=({x1_raw[i]:.1f}, {x2_raw[i]:.0f}) -> norm=({x1_norm[i]:.4f}, {x2_norm[i]:.4f})")
        
    print("\nInitial Centroids:")
    for k in range(3):
        print(f"C{k+1} (from {ids[init_indices[k]]}): ({centroids[k,0]:.4f}, {centroids[k,1]:.4f})")
        
    curr_centroids = centroids.copy()
    prev_assignments = None
    
    for round_num in range(1, 4):
        print(f"\n==================== ROUND {round_num} ====================")
        # Compute distances
        dists = np.zeros((len(points), 3))
        for k in range(3):
            dists[:, k] = np.sqrt(np.sum((points - curr_centroids[k])**2, axis=1))
            
        assignments = np.argmin(dists, axis=1) + 1 # 1, 2, 3
        
        # Check for ties or very close distances (< 0.005)
        for i in range(len(points)):
            sorted_d = np.sort(dists[i])
            if sorted_d[1] - sorted_d[0] < 0.01:
                print(f"WARNING: Close call for {ids[i]}: diff = {sorted_d[1] - sorted_d[0]:.4f}")
                
        # Compute min distance squared
        min_d = np.min(dists, axis=1)
        wcss = np.sum(min_d**2)
        
        print(f"{'ID':<6} {'d(P,C1)':<10} {'d(P,C2)':<10} {'d(P,C3)':<10} {'Cluster':<8} {'d_min^2':<10}")
        print("-" * 56)
        for i in range(len(points)):
            print(f"{ids[i]:<6} {dists[i,0]:<10.4f} {dists[i,1]:<10.4f} {dists[i,2]:<10.4f} Cluster {assignments[i]:<2} {min_d[i]**2:<10.4f}")
        print(f"Total WCSS (Inertia) = {wcss:.6f}")
        
        # Cluster counts
        counts = [np.sum(assignments == k) for k in [1, 2, 3]]
        print(f"Cluster counts: C1={counts[0]}, C2={counts[1]}, C3={counts[2]}")
        if any(c == 0 for c in counts):
            print("ERROR: Empty cluster detected!")
            return False
            
        # Update centroids
        new_centroids = np.zeros((3, 2))
        for k in range(3):
            cluster_pts = points[assignments == (k + 1)]
            new_centroids[k] = np.mean(cluster_pts, axis=0)
            print(f"New C{k+1}: ({new_centroids[k,0]:.4f}, {new_centroids[k,1]:.4f}) [n={len(cluster_pts)}]")
            
        if prev_assignments is not None:
            changed = np.sum(assignments != prev_assignments)
            print(f"Points changed cluster from previous round: {changed}")
        prev_assignments = assignments.copy()
        curr_centroids = new_centroids.copy()
        
    return True

# Let's test candidate
raw_data_1 = [
    ("S01", 2, 10000),
    ("S02", 4, 15000),
    ("S03", 6, 20000),
    ("S04", 10, 30000),
    ("S05", 12, 35000),
    ("S06", 14, 40000),
    ("S07", 18, 50000),
    ("S08", 20, 55000),
    ("S09", 22, 60000),
]
print("--- TESTING CANDIDATE 1 ---")
run_kmeans_sim(raw_data_1, [0, 3, 8], ["Frequency", "Spending"])
