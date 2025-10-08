# Example from: docs\mathematical_foundations\controller_comparison_theory.md
# Index: 4
# Runnable: False
# Hash: e9bb8d1b

# example-metadata:
# runnable: false

def compute_control_hybrid(state, k1_prev, k2_prev, u_int_prev):
    # 1. Sliding surface (with cart recentering)
    sigma = c1*(dth1+lam1*th1) + c2*(dth2+lam2*th2) + kc*(dx+lamc*x)  # ~18 ops

    # 2. Equivalent control
    u_eq = ...  # ~80 ops

    # 3. Adaptive gain updates (both k1 and k2)
    taper = abs(sigma) / (abs(sigma) + eps_taper)  # ~5 ops
    k1_dot = gamma1 * abs(sigma) * taper  # ~3 ops
    k2_dot = gamma2 * abs(sigma) * taper  # ~3 ops
    k1_new = clip(k1_prev + k1_dot*dt, 0, k1_max)  # ~4 ops
    k2_new = clip(k2_prev + k2_dot*dt, 0, k2_max)  # ~4 ops

    # 4. Super-twisting control
    u_c = -k1_new * sqrt(abs(sigma)) * sat(sigma)  # ~10 ops
    u_int = clip(u_int_prev - k2_new*sat(sigma)*dt, -umax, umax)  # ~5 ops
    u_d = -k_d * sigma  # ~2 ops

    # Total: ~134 ops