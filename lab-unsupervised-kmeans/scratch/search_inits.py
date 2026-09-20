import numpy as np

# Let's search for points that give clean numbers
# Suppose we have 9 points:
# C1 group: P1=(0.0, 0.0), P2=(0.1, 0.2), P3=(0.2, 0.1)
# C2 group: P4=(0.4, 0.5), P5=(0.5, 0.5), P6=(0.6, 0.6)
# C3 group: P7=(0.8, 0.9), P8=(0.9, 0.8), P9=(1.0, 1.0)
# What if initial centroids are NOT P1, P4, P9, but chosen so that one point starts in another cluster?
# For example, initial centroids:
# C1 = P1 (0.0, 0.0)
# C2 = P6 (0.6, 0.6)
# C3 = P9 (1.0, 1.0)
# Let's test!

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

for i1 in range(len(pts)):
    for i2 in range(i1+1, len(pts)):
        for i3 in range(i2+1, len(pts)):
            inits = (i1, i2, i3)
            centroids = pts[list(inits)].copy()
            history = []
            valid = True
            for r in range(3):
                dists = np.zeros((len(pts), 3))
                for k in range(3):
                    dists[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
                sort_d = np.sort(dists, axis=1)
                margin = np.min(sort_d[:, 1] - sort_d[:, 0])
                if margin < 0.03:
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
                    'margin': margin,
                    'wcss': np.sum(dmin**2),
                    'c': centroids.copy(),
                    'new_c': new_c.copy()
                })
                centroids = new_c.copy()
            if valid and len(history) == 3:
                c1 = np.sum(history[0]['assign'] != history[1]['assign'])
                c2 = np.sum(history[1]['assign'] != history[2]['assign'])
                overall_margin = min(h['margin'] for h in history)
                if c1 > 0 and c2 == 0 and overall_margin >= 0.035:
                    print(f"Inits {inits} (P{i1+1}, P{i2+1}, P{i3+1}): c1={c1}, c2={c2}, min_margin={overall_margin:.4f}")
                    print(f"  R1 assign: {history[0]['assign']}")
                    print(f"  R2 assign: {history[1]['assign']}")
                    print(f"  R3 assign: {history[2]['assign']}")
