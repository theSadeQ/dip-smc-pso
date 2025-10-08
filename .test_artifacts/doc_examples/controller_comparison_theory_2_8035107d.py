# Example from: docs\mathematical_foundations\controller_comparison_theory.md
# Index: 2
# Runnable: False
# Hash: 8035107d

# example-metadata:
# runnable: false

def compute_control_adaptive(state, K_prev):
    # 1. Sliding surface
    sigma = ...  # ~10 ops

    # 2. Equivalent control
    u_eq = ...  # ~80 ops (same as classical)

    # 3. Adaptive gain update
    if abs(sigma) > delta:
        K_dot = gamma * abs(sigma)  # ~3 ops
    else:
        K_dot = -alpha * K_prev  # ~2 ops
    K_new = K_prev + K_dot * dt  # ~2 ops

    # 4. Switching term
    u_sw = -K_new * tanh(sigma/eps)  # ~5 ops

    # Total: ~102 ops