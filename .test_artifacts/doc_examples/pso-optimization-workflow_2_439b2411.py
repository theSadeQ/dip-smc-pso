# Example from: docs\guides\workflows\pso-optimization-workflow.md
# Index: 2
# Runnable: True
# Hash: 439b2411

# Velocity update
v[i] = w·v[i] + c1·r1·(pbest[i] - x[i]) + c2·r2·(gbest - x[i])
     = 0.7·v[i] + 2.0·r1·(pbest[i] - x[i]) + 2.0·r2·(gbest - x[i])

# Position update
x[i] = x[i] + v[i]
x[i] = clamp(x[i], lower_bounds, upper_bounds)