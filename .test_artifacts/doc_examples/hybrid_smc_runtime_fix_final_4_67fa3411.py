# Example from: docs\troubleshooting\hybrid_smc_runtime_fix_final.md
# Index: 4
# Runnable: False
# Hash: 67fa3411

# example-metadata:
# runnable: false

# Ensured all code paths have explicit returns
def compute_control(self, state, state_vars=None, history=None):
    # ... control computation logic ...

    # CRITICAL: Always return HybridSTAOutput
    return HybridSTAOutput(
        control=u_sat,
        state_vars=(k1_new, k2_new, u_int_new),
        history=history,
        sliding_surface=float(s)
    )