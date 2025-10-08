# Example from: docs\testing\guides\control_systems_unit_testing.md
# Index: 14
# Runnable: False
# Hash: 37c95a06

# example-metadata:
# runnable: false

def create_test_controller():
    """Create controller with optimal gains for testing."""
    optimal_gains = [77.62, 44.45, 17.31, 14.25, 18.66, 9.76]

    return ClassicalSMC(
        gains=optimal_gains,
        max_force=20.0,
        boundary_layer=9.76,
        switch_method='tanh',
        regularization=1e-10
    )