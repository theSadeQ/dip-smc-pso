# Example from: docs\troubleshooting\hybrid_smc_runtime_fix.md
# Index: 10
# Runnable: False
# Hash: 471ffdab

# Return type validation
def compute_control(self, state, state_vars, history) -> HybridSTAOutput:
    # Implementation ensures return type matches annotation
    result = HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

    # Type assertion for runtime verification
    assert isinstance(result, HybridSTAOutput)
    assert isinstance(result.control, float)
    assert len(result.state_vars) == 3
    assert isinstance(result.history, dict)
    assert isinstance(result.sliding_surface, float)

    return result