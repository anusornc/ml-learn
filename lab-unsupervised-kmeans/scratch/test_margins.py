import numpy as np

pts_list = []
# Let's test a simple setup:
# Suppose we have 9 points:
# C1: P1=(0.1, 0.1), P2=(0.1, 0.2), P3=(0.2, 0.1)
# C2: P4=(0.4, 0.5), P5=(0.5, 0.6), P6=(0.6, 0.5)
# C3: P7=(0.8, 0.8), P8=(0.8, 0.9), P9=(0.9, 0.8)

# Now what happens if we set initial centroids?
# Let's write a script that tests various points and inits
pts = np.array([
    [0.1, 0.1], # P1
    [0.1, 0.3], # P2
    [0.2, 0.1], # P3
    [0.4, 0.4], # P4
    [0.5, 0.6], # P5
    [0.6, 0.5], # P6
    [0.7, 0.8], # P7
    [0.8, 0.9], # P8
    [0.9, 0.7], # P9
])

for inits in [(0, 3, 8), (0, 4, 8), (0, 5, 8), (1, 4, 7), (2, 4, 6), (0, 3, 7)]:
    centroids = pts[list(inits)].copy()
    print(f"\nTesting inits {inits}:")
    for r in range(3):
        d = np.zeros((len(pts), 3))
        for k in range(3):
            d[:, k] = np.sqrt(np.sum((pts - centroids[k])**2, axis=1))
        assign = np.argmin(d, axis=1) + 1
        mins = np.min(d, axis=1)
        sort_d = np.sort(d, axis=1)
        margin = np.min(sort_d[:, 1] - sort_d[:, 0])
        print(f"  R{r+1}: assign={assign}, min_margin={margin:.4f}, wcss={np.sum(mins**2):.4f}")
        for k in range(3):
            centroids[k] = np.mean(pts[assign == (k+1)], axis=0)
