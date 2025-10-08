# Example from: docs\mathematical_foundations\controller_comparison_theory.md
# Index: 1
# Runnable: False
# Hash: 2709eecd

# example-metadata:
# runnable: false

def compute_control_classical(state):
    # 1. Sliding surface (6 multiplications, 3 additions)
    sigma = lam1*th1 + lam2*th2 + k1*dth1 + k2*dth2  # ~10 ops

    # 2. Equivalent control (matrix inversion: O(n³) = 27 ops)
    M_inv = np.linalg.inv(M)  # ~50 ops (3×3 matrix)
    u_eq = (L @ M_inv @ B)^-1 * ...  # ~30 ops

    # 3. Switching term (saturation function)
    u_sw = -K * tanh(sigma/eps)  # ~5 ops

    # Total: ~95 ops