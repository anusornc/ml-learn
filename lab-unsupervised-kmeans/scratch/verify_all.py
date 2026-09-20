import numpy as np

# Dataset definition
raw_data = [
    ("P1", "สมคิด", 20, 15000),
    ("P2", "สมชาย", 24, 25000),
    ("P3", "สมหมาย", 28, 20000),
    ("P4", "กานดา", 36, 40000),
    ("P5", "เกศรา", 40, 40000),
    ("P6", "ขวัญใจ", 44, 45000),
    ("P7", "ฉัตรชัย", 52, 60000),
    ("P8", "ชัยวัฒน์", 56, 55000),
    ("P9", "ชูศักดิ์", 60, 65000),
]

names = [d[1] for d in raw_data]
pids = [d[0] for d in raw_data]
age_raw = np.array([d[2] for d in raw_data], dtype=float)
inc_raw = np.array([d[3] for d in raw_data], dtype=float)

min_age, max_age = np.min(age_raw), np.max(age_raw)
range_age = max_age - min_age

min_inc, max_inc = np.min(inc_raw), np.max(inc_raw)
range_inc = max_inc - min_inc

age_norm = (age_raw - min_age) / range_age
inc_norm = (inc_raw - min_inc) / range_inc

pts = np.column_stack([age_norm, inc_norm])

print("=======================================================================")
print("                   RIGOROUS VERIFICATION SCRIPT                        ")
print("=======================================================================")

print(f"Age: Min={min_age:.1f}, Max={max_age:.1f}, Range={range_age:.1f}")
print(f"Income: Min={min_inc:.0f}, Max={max_inc:.0f}, Range={range_inc:.0f}\n")

print("--- NORMALIZED DATA ---")
for i in range(len(raw_data)):
    print(f"{pids[i]} ({names[i]}): Age={age_raw[i]:.0f} -> {age_norm[i]:.4f} | Income={inc_raw[i]:,.0f} -> {inc_norm[i]:.4f}")

# Initial Centroids
c_init = pts[[0, 4, 8]].copy()
print("\n--- INITIAL CENTROIDS (t=0) ---")
print(f"C1 (from P1): ({c_init[0,0]:.4f}, {c_init[0,1]:.4f})")
print(f"C2 (from P5): ({c_init[1,0]:.4f}, {c_init[1,1]:.4f})")
print(f"C3 (from P9): ({c_init[2,0]:.4f}, {c_init[2,1]:.4f})")

curr_c = c_init.copy()
all_rounds = []

for r in range(1, 4):
    print(f"\n==================== ITERATION {r} ====================")
    print(f"Centroids at start of Round {r}:")
    for k in range(3):
        print(f"  C{k+1}: ({curr_c[k,0]:.4f}, {curr_c[k,1]:.4f})")
        
    d = np.zeros((len(pts), 3))
    for k in range(3):
        d[:, k] = np.sqrt((pts[:,0] - curr_c[k,0])**2 + (pts[:,1] - curr_c[k,1])**2)
        
    assign = np.argmin(d, axis=1) + 1
    dmin = np.min(d, axis=1)
    dmin_sq = dmin**2
    wcss = np.sum(dmin_sq)
    
    print(f"\n{'ID':<5} {'Name':<10} {'X1_norm':<9} {'X2_norm':<9} {'d(P,C1)':<10} {'d(P,C2)':<10} {'d(P,C3)':<10} {'Cluster':<8} {'d_min^2':<10}")
    print("-" * 80)
    for i in range(len(pts)):
        print(f"{pids[i]:<5} {names[i]:<10} {pts[i,0]:<9.4f} {pts[i,1]:<9.4f} {d[i,0]:<10.4f} {d[i,1]:<10.4f} {d[i,2]:<10.4f} Cluster {assign[i]:<1} {dmin_sq[i]:<10.4f}")
        
    print(f"\nTotal WCSS (Inertia) Round {r} = {wcss:.6f}")
    
    # Calculate new centroids
    new_c = np.zeros((3, 2))
    for k in range(3):
        idx_k = (assign == (k+1))
        new_c[k] = np.mean(pts[idx_k], axis=0)
        pts_in_k = [pids[j] for j in range(len(pts)) if assign[j] == (k+1)]
        print(f"New C{k+1}: ({new_c[k,0]:.4f}, {new_c[k,1]:.4f}) | Members: {pts_in_k} (N={len(pts_in_k)})")
        
    all_rounds.append({
        'centroids_in': curr_c.copy(),
        'dists': d.copy(),
        'assign': assign.copy(),
        'dmin_sq': dmin_sq.copy(),
        'wcss': wcss,
        'centroids_out': new_c.copy()
    })
    curr_c = new_c.copy()
