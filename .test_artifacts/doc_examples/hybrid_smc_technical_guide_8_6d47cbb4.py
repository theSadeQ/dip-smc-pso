# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 8
# Runnable: False
# Hash: 6d47cbb4

def compute_control(self, state, state_vars, history):
    # ... 674 lines of controller logic ...

    return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))

def reset(self) -> None:
    # ... reset logic only ...
    pass