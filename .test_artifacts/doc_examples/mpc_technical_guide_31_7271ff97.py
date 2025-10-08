# Example from: docs\controllers\mpc_technical_guide.md
# Index: 31
# Runnable: True
# Hash: 7271ff97

# 1. Add slew rate limit
mpc = MPCController(dynamics, max_du=10.0)  # 10 N/step

# 2. Increase input penalty
weights = MPCWeights(r_u=0.05)  # Up from 0.01

# 3. Tighten solver tolerance
prob.solve(solver=cp.OSQP, eps_abs=1e-6, eps_rel=1e-6)