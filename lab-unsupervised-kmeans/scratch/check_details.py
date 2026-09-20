import numpy as np

def detailed_check(pts, inits, name=""):
    print(f"\n=======================================================")
    print(f"DETAILED CHECK: {name}")
    print(f"=======================================================")
    centroids = pts[list(inits)].copy()
    
    for r in range(1, 4):
        print(f"\n--- ROUND {r} ---")
        print("Centroids at start of round:")
        for k in range(3):
            print(f"  C{k+1}: ({centroids[k,0]:.4f}, {centroids[k,1]:.4f})")
            
        dists = np.zeros((len(pts), 3))
        for k in range(3):
            dists[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
            
        assignments = np.argmin(dists, axis=1) + 1
        dmin = np.min(dists, axis=1)
        wcss = np.sum(dmin**2)
        
        print(f"{'Pt':<5} {'X1_norm':<8} {'X2_norm':<8} {'d(P,C1)':<10} {'d(P,C2)':<10} {'d(P,C3)':<10} {'Cluster':<8} {'Margin':<8} {'d_min^2':<8}")
        print("-" * 75)
        for i in range(len(pts)):
            s = np.sort(dists[i])
            margin = s[1] - s[0]
            print(f"P{i+1:<4} {pts[i,0]:<8.4f} {pts[i,1]:<8.4f} {dists[i,0]:<10.4f} {dists[i,1]:<10.4f} {dists[i,2]:<10.4f} C{assignments[i]:<7} {margin:<8.4f} {dmin[i]**2:<8.4f}")
        print(f"WCSS = {wcss:.6f}")
        
        new_centroids = np.zeros((3, 2))
        for k in range(3):
            c_pts = pts[assignments == (k+1)]
            new_centroids[k] = np.mean(c_pts, axis=0)
            print(f"New C{k+1} (mean of {len(c_pts)} pts): ({new_centroids[k,0]:.4f}, {new_centroids[k,1]:.4f})")
        centroids = new_centroids.copy()

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

detailed_check(pts, (0, 3, 8), "Inits P1, P4, P9")
detailed_check(pts, (2, 4, 6), "Inits P3, P5, P7")
