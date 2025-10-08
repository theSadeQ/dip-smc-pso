# Example from: docs\testing\guides\coverage_quality_gates_troubleshooting.md
# Index: 12
# Runnable: False
# Hash: 703a0f70

# example-metadata:
# runnable: false

   # Enhanced stability test
   def test_lyapunov_stability_mathematical_proof():
       """Validate Lyapunov stability conditions with mathematical rigor."""
       controller = ClassicalSMC(gains=[10, 8, 15, 12, 50, 5])

       # Test multiple initial conditions
       initial_conditions = generate_stability_test_conditions(n=100)

       for ic in initial_conditions:
           # Lyapunov function: V = 0.5 * s²
           trajectory = simulate_trajectory(controller, ic, duration=5.0)
           lyapunov_values = [0.5 * compute_sliding_surface(state)**2
                            for state in trajectory]

           # V̇ ≤ 0 (non-increasing Lyapunov function)
           for i in range(1, len(lyapunov_values)):
               assert lyapunov_values[i] <= lyapunov_values[i-1] + 1e-6, \
                   f"Lyapunov function not decreasing at step {i}"