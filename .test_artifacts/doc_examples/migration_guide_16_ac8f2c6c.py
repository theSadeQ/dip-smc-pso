# Example from: docs\factory\migration_guide.md
# Index: 16
# Runnable: True
# Hash: ac8f2c6c

# Test migrated configuration with sample scenarios
test_scenarios = [
    np.array([0.1, 0.1, 0.1, 0.0, 0.0, 0.0]),  # Small disturbance
    np.array([0.3, 0.4, 0.2, 0.1, 0.0, 0.0]),  # Medium angles
]

for scenario in test_scenarios:
    control_output = migrated_controller.compute_control(scenario, (), {})
    assert np.isfinite(control_output.u), "Control output must be finite"