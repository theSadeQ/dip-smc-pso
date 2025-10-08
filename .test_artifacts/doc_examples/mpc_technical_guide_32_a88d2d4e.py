# Example from: docs\controllers\mpc_technical_guide.md
# Index: 32
# Runnable: True
# Hash: a88d2d4e

# 1. Install cvxpy
pip install cvxpy

# 2. Verify installation
import cvxpy as cp
print(cp.installed_solvers())  # Should include OSQP, ECOS, SCS

# 3. If installation fails, MPC degrades gracefully
mpc = MPCController(
    dynamics,
    fallback_smc_gains=[10, 8, 15, 12, 50, 5],
    fallback_boundary_layer=0.01
)
# Will use SMC when cvxpy unavailable