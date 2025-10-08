# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 10
# Runnable: True
# Hash: 94861a95

def test_hybrid_controller_return_type():
    """Validate hybrid controller returns proper types."""
    controller = HybridAdaptiveSTASMC(gains=[10, 5, 8, 3])

    state = np.zeros(6)
    result = controller.compute_control(state)

    assert isinstance(result, HybridSTAOutput)
    assert len(result.state_vars) == 3  # (k1, k2, u_int)
    assert isinstance(result.control, float)