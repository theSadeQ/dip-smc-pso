# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 16
# Runnable: True
# Hash: 6992f238

from src.plant.core import NumericalStabilityMonitor

monitor = NumericalStabilityMonitor()

# Simulation loop
for i in range(1000):
    M = physics.compute_inertia_matrix(states[i])
    cond_num = np.linalg.cond(M)

    regularized = not regularizer.check_conditioning(M)

    try:
        q_ddot = inverter.solve_linear_system(M, forcing[i])
        monitor.record_inversion(cond_num, regularized, failed=False)
    except NumericalInstabilityError:
        monitor.record_inversion(cond_num, regularized, failed=True)

# Get statistics
stats = monitor.get_statistics()
print(f"Simulation used regularization {stats['regularization_rate'] * 100:.1f}% of the time")
print(f"Max condition number: {stats['max_condition_number']:.2e}")
print(f"Failure rate: {stats['failed_count'] / stats['total_inversions'] * 100:.2f}%")