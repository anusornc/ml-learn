import numpy as np

# Let's search for points on a grid [0.0, 0.1, ..., 1.0]
# 9 points, 3 in cluster 1, 3 in cluster 2, 3 in cluster 3
# Let's see if we can find inits where a point switches in Round 2 with margin >= 0.08 in all rounds
found = []

for p1 in [[0.0, 0.0], [0.0, 0.1]]:
    for p2 in [[0.1, 0.2], [0.2, 0.0]]:
        for p3 in [[0.2, 0.1], [0.1, 0.1]]:
            for p4 in [[0.3, 0.4], [0.4, 0.4], [0.35, 0.35]]:
                for p5 in [[0.5, 0.5], [0.5, 0.6]]:
                    for p6 in [[0.6, 0.5], [0.6, 0.6]]:
                        for p7 in [[0.7, 0.8], [0.8, 0.7], [0.75, 0.75]]:
                            for p8 in [[0.9, 0.8], [0.8, 0.9]]:
                                for p9 in [[1.0, 1.0], [1.0, 0.9]]:
                                    pts = np.array([p1, p2, p3, p4, p5, p6, p7, p8, p9])
                                    if pts[:,0].min() != 0.0 or pts[:,0].max() != 1.0: continue
                                    if pts[:,1].min() != 0.0 or pts[:,1].max() != 1.0: continue
                                    
                                    for inits in [(0, 3, 5), (0, 4, 7), (1, 4, 8), (0, 3, 8), (0, 4, 8), (0, 5, 8)]:
                                        centroids = pts[list(inits)].copy()
                                        valid = True
                                        history = []
                                        for r in range(3):
                                            dists = np.zeros((9, 3))
                                            for k in range(3):
                                                dists[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
                                            sort_d = np.sort(dists, axis=1)
                                            m = np.min(sort_d[:, 1] - sort_d[:, 0])
                                            if m < 0.07:
                                                valid = False
                                                break
                                            assign = np.argmin(dists, axis=1) + 1
                                            counts = [np.sum(assign == k) for k in [1, 2, 3]]
                                            if any(c < 2 for c in counts):
                                                valid = False
                                                break
                                            new_c = np.zeros((3, 2))
                                            for k in range(3):
                                                new_c[k] = np.mean(pts[assign == (k+1)], axis=0)
                                            dmin = np.min(dists, axis=1)
                                            history.append({
                                                'assign': assign.copy(),
                                                'margin': m,
                                                'wcss': np.sum(dmin**2),
                                                'c': centroids.copy(),
                                                'new_c': new_c.copy()
                                            })
                                            centroids = new_c.copy()
                                        if valid and len(history) == 3:
                                            c1 = np.sum(history[0]['assign'] != history[1]['assign'])
                                            c2 = np.sum(history[1]['assign'] != history[2]['assign'])
                                            if c1 >= 1 and c2 == 0:
                                                overall_m = min(h['margin'] for h in history)
                                                found.append((overall_m, pts.copy(), inits, history))

print(f"Found with shift: {len(found)}")
if found:
    found.sort(key=lambda x: x[0], reverse=True)
    best_m, pts, inits, hist = found[0]
    print(f"Best min margin: {best_m:.4f}")
    print(f"Inits: {inits}")
    print(f"Points:\n{pts}")
    for r in range(3):
        print(f"R{r+1}: assign={hist[r]['assign']}, margin={hist[r]['margin']:.4f}, wcss={hist[r]['wcss']:.4f}")
