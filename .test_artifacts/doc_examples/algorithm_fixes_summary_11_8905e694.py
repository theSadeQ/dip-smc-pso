# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 11
# Runnable: False
# Hash: 8905e694

# example-metadata:
# runnable: false

   def test_computation_precision_consistency(self):
       """Test that repeated computations maintain precision."""
       config = ClassicalSMCConfig(
           gains=[5.0, 3.0, 4.0, 2.0, 10.0, 1.0],
           max_force=100.0, dt=0.01, boundary_layer=0.01
       )
       controller = ModularClassicalSMC(config=config)

       state = np.array([0.123456789, 0.987654321, 0.456789123, 0.321654987, 0.789123456, 0.654987321])

       # Compute control 1000 times
       results = []
       for _ in range(1000):
           result = controller.compute_control(state, {}, {})
           control = result.get('control_output', result.get('control', 0))
           results.append(control)

       results = np.array(results)

       # Standard deviation should be zero (deterministic computation)
       std_dev = np.std(results, axis=0) if results.ndim > 1 else np.std(results)
       assert np.all(std_dev < 1e-15)  # Machine precision level