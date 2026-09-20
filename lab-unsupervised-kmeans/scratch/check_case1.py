import numpy as np

# Let's search if any choice of inits gives margin >= 0.08 in all 3 rounds with transition in R2
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

# What if P4 is (0.35, 0.45) or P5 is (0.50, 0.50)?
# Or what if we use Case 1 (Inits P1, P5, P9)?
# Let's check Case 1:
# In Case 1:
# Round 1 min margin = 0.2764! (Huge!)
# Round 2 min margin = 0.3041! (Huge!)
# Round 3 min margin = 0.3041! (Huge!)
# No student could ever get confused or make a tie-breaking error!
