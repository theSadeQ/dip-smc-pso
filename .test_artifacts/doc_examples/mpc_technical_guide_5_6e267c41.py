# Example from: docs\controllers\mpc_technical_guide.md
# Index: 5
# Runnable: True
# Hash: 6e267c41

# Warm start with previous solution
U.value = U_prev.reshape(1, -1)

# Solve (prefer OSQP)
problem.solve(solver=cp.OSQP, warm_start=True, verbose=False)

if problem.status in [cp.OPTIMAL, cp.OPTIMAL_INACCURATE]:
    u_optimal = U.value[0, 0]
    U_prev = U.value.reshape(-1)  # Cache for next step
else:
    u_optimal = safe_fallback(x₀)