import numpy as np

# Let's search over variations to find the absolute cleanest exam numbers!
candidates = []

for p3_x, p3_y in [(0.2, 0.1), (0.2, 0.15), (0.15, 0.2), (0.2, 0.25)]:
    for p4_x, p4_y in [(0.35, 0.35), (0.35, 0.4), (0.4, 0.35), (0.4, 0.4), (0.3, 0.35), (0.3, 0.45)]:
        for p7_x, p7_y in [(0.7, 0.7), (0.7, 0.75), (0.75, 0.7), (0.65, 0.7)]:
            pts = np.array([
                [0.0, 0.1],   # P1
                [0.1, 0.0],   # P2
                [p3_x, p3_y], # P3
                [p4_x, p4_y], # P4
                [0.5, 0.5],   # P5
                [0.6, 0.4],   # P6
                [p7_x, p7_y], # P7
                [0.9, 1.0],   # P8
                [1.0, 0.9],   # P9
            ])
            
            # test initial centroids
            for inits in [(0, 3, 8), (0, 4, 8), (1, 4, 7), (0, 4, 7), (2, 4, 6), (0, 5, 8)]:
                centroids = pts[list(inits)].copy()
                valid = True
                history = []
                
                for r in range(3):
                    dists = np.zeros((len(pts), 3))
                    for k in range(3):
                        dists[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
                    
                    min_margin = 999.0
                    for i in range(len(pts)):
                        s = np.sort(dists[i])
                        m = s[1] - s[0]
                        if m < min_margin:
                            min_margin = m
                    if min_margin < 0.04:
                        valid = False
                        break
                        
                    assignments = np.argmin(dists, axis=1) + 1
                    counts = [np.sum(assignments == k) for k in [1, 2, 3]]
                    if any(c < 2 for c in counts):
                        valid = False
                        break
                        
                    new_centroids = np.zeros((3, 2))
                    for k in range(3):
                        new_centroids[k] = np.mean(pts[assignments == (k+1)], axis=0)
                    dmin = np.min(dists, axis=1)
                    wcss = np.sum(dmin**2)
                    history.append({
                        'assignments': assignments.copy(),
                        'centroids': centroids.copy(),
                        'new_centroids': new_centroids.copy(),
                        'margin': min_margin,
                        'wcss': wcss
                    })
                    centroids = new_centroids.copy()
                    
                if not valid or len(history) < 3:
                    continue
                    
                c1 = np.sum(history[0]['assignments'] != history[1]['assignments'])
                c2 = np.sum(history[1]['assignments'] != history[2]['assignments'])
                
                if (c1 in [1, 2]) and c2 == 0:
                    overall_min_margin = min(history[r]['margin'] for r in range(3))
                    candidates.append((overall_min_margin, pts, inits, history))

print(f"Total candidates found: {len(candidates)}")
if candidates:
    candidates.sort(key=lambda x: x[0], reverse=True)
    best_margin, best_pts, best_inits, best_hist = candidates[0]
    print(f"Best minimum margin across all rounds: {best_margin:.4f}")
    print(f"Initial centroids: {best_inits} -> P{best_inits[0]+1}, P{best_inits[1]+1}, P{best_inits[2]+1}")
    print("Points:")
    for i, p in enumerate(best_pts):
        print(f"  P{i+1}: ({p[0]:.2f}, {p[1]:.2f})")
    for r in range(3):
        print(f"\n--- Round {r+1} ---")
        print(f"  Assignments: {best_hist[r]['assignments']}")
        print(f"  Min Margin: {best_hist[r]['margin']:.4f}")
        print(f"  WCSS: {best_hist[r]['wcss']:.4f}")
        print(f"  New Centroids: C1={best_hist[r]['new_centroids'][0]}, C2={best_hist[r]['new_centroids'][1]}, C3={best_hist[r]['new_centroids'][2]}")
