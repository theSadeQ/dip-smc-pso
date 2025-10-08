# Example from: docs\testing\guides\property_based_testing.md
# Index: 1
# Runnable: True
# Hash: f5a49a68

def test_smc_zero_error():
    """Test SMC with zero error"""
    state = [0, 0, 0, 0]  # Specific case
    control = smc.compute_control(state)
    assert control == 0