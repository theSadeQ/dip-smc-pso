# Example from: docs\mathematical_foundations\controller_comparison_theory.md
# Index: 3
# Runnable: False
# Hash: b5bed29f

# example-metadata:
# runnable: false

def compute_control_sta(state, u_int_prev):
    # 1. Sliding surface
    sigma = ...  # ~10 ops

    # 2. Equivalent control
    u_eq = ...  # ~80 ops

    # 3. Continuous term (square root!)
    u_c = -K1 * sqrt(abs(sigma)) * sign(sigma)  # ~10 ops (sqrt expensive)

    # 4. Integral term update
    u_int = u_int_prev - K2 * sign(sigma) * dt  # ~3 ops

    # 5. Damping term
    u_d = -k_d * sigma  # ~2 ops

    # Total: ~105 ops