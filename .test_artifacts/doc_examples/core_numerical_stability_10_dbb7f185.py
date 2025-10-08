# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 10
# Runnable: True
# Hash: dbb7f185

from src.plant.core import NumericalStabilityMonitor

monitor = NumericalStabilityMonitor()

# During simulation loop
for t in time_steps:
    M = physics.compute_inertia_matrix(state)
    cond_num = np.linalg.cond(M)
    regularized = cond_num > 1e12

    try:
        M_inv = inverter.invert_matrix(M)
        monitor.record_inversion(cond_num, regularized, failed=False)
    except NumericalInstabilityError:
        monitor.record_inversion(cond_num, regularized, failed=True)