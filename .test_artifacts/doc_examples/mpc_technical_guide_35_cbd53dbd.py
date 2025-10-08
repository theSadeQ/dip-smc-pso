# Example from: docs\controllers\mpc_technical_guide.md
# Index: 35
# Runnable: True
# Hash: cbd53dbd

# Compare cold vs warm start
t0 = time.time()
prob.solve(solver=cp.OSQP, warm_start=False)
t_cold = time.time() - t0

t0 = time.time()
prob.solve(solver=cp.OSQP, warm_start=True)
t_warm = time.time() - t0

print(f"Speedup: {t_cold/t_warm:.1f}×")