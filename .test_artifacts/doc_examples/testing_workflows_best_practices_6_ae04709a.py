# Example from: docs\testing\testing_workflows_best_practices.md
# Index: 6
# Runnable: False
# Hash: ae04709a

# Identify uncovered code
# src/controllers/smc/classic_smc.py:89-92 not covered

# Lines 89-92: Error handling for invalid state
if np.any(np.isnan(state)):
    raise ValueError("State contains NaN values")
if np.any(np.isinf(state)):
    raise ValueError("State contains infinite values")

# Write test to cover this code
def test_nan_state_rejection():
    """Test that NaN states are rejected."""
    controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100)

    nan_state = np.array([0.1, np.nan, 0.08, 0.02, 0.03, 0.01])

    with pytest.raises(ValueError, match="NaN values"):
        controller.compute_control(nan_state, {}, {})

def test_inf_state_rejection():
    """Test that infinite states are rejected."""
    controller = ClassicalSMC(gains=[10,8,15,12,50,5], max_force=100)

    inf_state = np.array([0.1, np.inf, 0.08, 0.02, 0.03, 0.01])

    with pytest.raises(ValueError, match="infinite values"):
        controller.compute_control(inf_state, {}, {})

# Run coverage again → Lines 89-92 now covered