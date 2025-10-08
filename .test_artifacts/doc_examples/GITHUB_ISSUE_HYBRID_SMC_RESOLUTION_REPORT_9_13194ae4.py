# Example from: docs\reports\GITHUB_ISSUE_HYBRID_SMC_RESOLUTION_REPORT.md
# Index: 9
# Runnable: False
# Hash: 13194ae4

def compute_control(self, state, state_vars=None, history=None) -> HybridSTAOutput:
    """Compute control with runtime validation."""

    # ... control algorithm implementation ...

    result = HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

    # Development mode validation
    if __debug__:
        assert isinstance(result, HybridSTAOutput)
        assert isinstance(result.control, (int, float))
        assert len(result.state_vars) == 3
        assert isinstance(result.history, dict)
        assert np.isfinite(result.control)

    return result