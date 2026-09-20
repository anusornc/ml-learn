import numpy as np

pts = np.array([
    [0.0, 0.0],  # P1
    [0.1, 0.2],  # P2
    [0.2, 0.1],  # P3
    [0.4, 0.5],  # P4
    [0.5, 0.5],  # P5
    [0.6, 0.6],  # P6
    [0.8, 0.9],  # P7
    [0.9, 0.8],  # P8
    [1.0, 1.0],  # P9
])

def run_case(inits, name):
    print(f"\n=======================================================")
    print(f"CASE: {name} (Inits: {[f'P{i+1}' for i in inits]})")
    print(f"=======================================================")
    centroids = pts[list(inits)].copy()
    for r in range(1, 4):
        print(f"\n--- ROUND {r} ---")
        print("Centroids at start:")
        for k in range(3):
            print(f"  C{k+1}: ({centroids[k,0]:.4f}, {centroids[k,1]:.4f})")
        dists = np.zeros((len(pts), 3))
        for k in range(3):
            dists[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
        assign = np.argmin(dists, axis=1) + 1
        dmin = np.min(dists, axis=1)
        sort_d = np.sort(dists, axis=1)
        margin = sort_d[:, 1] - sort_d[:, 0]
        
        print(f"{'Pt':<5} {'d(P,C1)':<10} {'d(P,C2)':<10} {'d(P,C3)':<10} {'Cluster':<8} {'Margin':<8} {'d_min^2':<8}")
        print("-" * 65)
        for i in range(len(pts)):
            print(f"P{i+1:<4} {dists[i,0]:<10.4f} {dists[i,1]:<10.4f} {dists[i,2]:<10.4f} C{assign[i]:<7} {margin[i]:<8.4f} {dmin[i]**2:<8.4f}")
        wcss = np.sum(dmin**2)
        print(f"WCSS = {wcss:.6f}")
        new_c = np.zeros((3, 2))
        for k in range(3):
            c_pts = pts[assign == (k+1)]
            new_c[k] = np.mean(c_pts, axis=0)
            print(f"New C{k+1} (mean of {len(c_pts)} pts): ({new_c[k,0]:.4f}, {new_c[k,1]:.4f})")
        centroids = new_c.copy()

run_case((0, 4, 8), "Initial Seeds P1, P5, P9 (Natural Seeds: Min, Mid, Max)")
run_case((0, 3, 5), "Initial Seeds P1, P4, P6 (With 1 point transition in R2)")
