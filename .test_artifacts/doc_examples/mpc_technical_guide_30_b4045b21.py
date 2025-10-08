# Example from: docs\controllers\mpc_technical_guide.md
# Index: 30
# Runnable: True
# Hash: b4045b21

# 1. Ensure warm start enabled
prob.solve(solver=cp.OSQP, warm_start=True)

# 2. Reduce horizon
mpc = MPCController(dynamics, horizon=12)  # Down from 20

# 3. Profile solvers
import time
t0 = time.time()
prob.solve(solver=cp.OSQP)
print(f"OSQP: {(time.time()-t0)*1000:.2f} ms")