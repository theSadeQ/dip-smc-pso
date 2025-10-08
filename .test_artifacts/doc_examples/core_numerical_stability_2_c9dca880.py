# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 2
# Runnable: True
# Hash: c9dca880

try:
    q_ddot = solver.solve_linear_system(M, forcing)
except NumericalInstabilityError as e:
    logger.error(f"Dynamics computation failed: {e}")
    # Fallback: use previous state or safe default