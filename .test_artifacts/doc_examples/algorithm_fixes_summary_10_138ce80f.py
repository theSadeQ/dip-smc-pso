# Example from: docs\mathematical_foundations\algorithm_fixes_summary.md
# Index: 10
# Runnable: False
# Hash: 138ce80f

# example-metadata:
# runnable: false

   def test_numerical_stability_extreme_values(self):
       """Test behavior with extreme but valid parameter values."""

       # Very small gains (but above minimum threshold)
       small_gains = [1e-10, 1e-10, 1e-10, 1e-10, 1e-8, 0.0]
       config_small = ClassicalSMCConfig(gains=small_gains, max_force=1e-6, dt=1e-6, boundary_layer=1e-8)

       # Very large gains
       large_gains = [1e6, 1e6, 1e6, 1e6, 1e8, 1e4]
       config_large = ClassicalSMCConfig(gains=large_gains, max_force=1e8, dt=1e-3, boundary_layer=1.0)

       # Both should create valid controllers
       controller_small = ModularClassicalSMC(config=config_small)
       controller_large = ModularClassicalSMC(config=config_large)

       # Test with moderate state values
       state = np.array([0.1, 0.05, 0.08, 0.02, 0.03, 0.01])

       result_small = controller_small.compute_control(state, {}, {})
       result_large = controller_large.compute_control(state, {}, {})

       # Both should produce finite, bounded results
       assert np.all(np.isfinite(result_small.get('control_output', [0])))
       assert np.all(np.isfinite(result_large.get('control_output', [0])))