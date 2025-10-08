# Example from: docs\controllers\mpc_technical_guide.md
# Index: 14
# Runnable: False
# Hash: 33f19241

# example-metadata:
# runnable: false

# Solve with warm start
try:
    prob.solve(solver=cp.OSQP, warm_start=True, verbose=False)
except:
    prob.solve(warm_start=True, verbose=False)  # Fallback solver

# Check status
if prob.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
    logger.warning("MPC failed (%s), using fallback", prob.status)
    return self._safe_fallback(x0)

# Extract and cache solution
u0 = float(U.value[0, 0])
self._U_prev = U.value.reshape(-1)  # Warm start next solve

# Apply slew rate limit if configured
if self._max_du is not None:
    du = np.clip(u0 - self._last_u_out, -self._max_du, self._max_du)
    u0 = self._last_u_out + du

self._last_u_out = u0
return float(np.clip(u0, -self.max_force, self.max_force))