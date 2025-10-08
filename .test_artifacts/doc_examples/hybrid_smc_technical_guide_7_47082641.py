# Example from: docs\controllers\hybrid_smc_technical_guide.md
# Index: 7
# Runnable: False
# Hash: 47082641

def compute_control(self, state, state_vars, history):
    # ... 674 lines of controller logic ...

    # Missing return statement here!

def reset(self) -> None:
    # ... reset logic ...
    return HybridSTAOutput(u_sat, (k1_new, k2_new, u_int_new), history, float(s))
    # ^^^^ Variables not in scope! ^^^^