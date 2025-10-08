# Example from: docs\controllers\mpc_technical_guide.md
# Index: 29
# Runnable: False
# Hash: dc05f94c

# Relax angle constraints
mpc = MPCController(
    dynamics,
    max_theta_dev=0.7,  # Increase from 0.5
    max_force=30.0      # Increase force limit
)

# Check state before solve
if abs(x[1] - np.pi) > 0.4:
    logger.warning("State near linearization limits")
    u = mpc._safe_fallback(x)  # Use fallback explicitly