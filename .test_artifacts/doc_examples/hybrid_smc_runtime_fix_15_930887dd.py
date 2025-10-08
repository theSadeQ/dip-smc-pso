# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 15
# Runnable: False
# Hash: 930887dd

# example-metadata:
# runnable: false

# Enhanced HybridAdaptiveSTASMC with runtime validation
def compute_control(self, state, state_vars, history) -> HybridSTAOutput:
    """Compute control with runtime type validation."""

    # ... control algorithm implementation ...

    # Prepare return value
    result = HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

    # Runtime validation (development mode)
    if __debug__:
        assert isinstance(result, HybridSTAOutput), f"Expected HybridSTAOutput, got {type(result)}"
        assert isinstance(result.control, (int, float)), f"Control must be numeric, got {type(result.control)}"
        assert len(result.state_vars) == 3, f"Expected 3 state vars, got {len(result.state_vars)}"
        assert isinstance(result.history, dict), f"History must be dict, got {type(result.history)}"
        assert np.isfinite(result.control), f"Control must be finite, got {result.control}"

    return result