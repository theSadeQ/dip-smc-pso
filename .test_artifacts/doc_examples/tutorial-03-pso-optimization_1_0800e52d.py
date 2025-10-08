# Example from: docs\guides\tutorials\tutorial-03-pso-optimization.md
# Index: 1
# Runnable: True
# Hash: 0800e52d

# Velocity update
v[i] = w·v[i] + c1·r1·(pbest[i] - x[i]) + c2·r2·(gbest - x[i])
       ↑        ↑                         ↑
       inertia  cognitive component       social component

# Position update
x[i] = x[i] + v[i]