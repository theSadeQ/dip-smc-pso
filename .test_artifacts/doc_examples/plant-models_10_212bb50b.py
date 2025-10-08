# Example from: docs\guides\api\plant-models.md
# Index: 10
# Runnable: False
# Hash: 212bb50b

# example-metadata:
# runnable: false

def validate_custom_dynamics(dynamics):
    """Ensure custom dynamics satisfy basic properties."""
    state = np.array([0, 0, 0.1, 0, 0.15, 0])
    control = 0.0

    # Test 1: State derivative has correct shape
    state_dot = dynamics.compute_dynamics(state, control)
    assert state_dot.shape == (6,), "State derivative shape mismatch"

    # Test 2: No NaN or Inf
    assert np.all(np.isfinite(state_dot)), "Invalid values in state derivative"

    # Test 3: Energy conservation (no control, no friction)
    # ... implement energy check

    print("Custom dynamics validation passed!")

validate_custom_dynamics(custom_dynamics)