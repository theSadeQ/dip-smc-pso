# Example from: docs\testing\guides\property_based_testing.md
# Index: 2
# Runnable: True
# Hash: ec6ec8eb

@given(state=states())
def test_smc_bounded_output(state):
    """Test SMC output always bounded"""
    control = smc.compute_control(state)
    assert -MAX_TORQUE <= control <= MAX_TORQUE  # For ALL states