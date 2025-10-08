# Example from: docs\reference\plant\core___init__.md
# Index: 2
# Runnable: False
# Hash: 2bbabcfb

# example-metadata:
# runnable: false

def dynamics_step(x, u, params):
    q, q_dot = extract_coordinates(x)
    M = compute_mass_matrix(q, params)
    C = compute_coriolis_matrix(q, q_dot, params)
    G = compute_gravity_vector(q, params)
    M_inv = robust_inverse(M)
    q_ddot = M_inv @ (B @ u - C @ q_dot - G)
    x_dot = assemble_state_derivative(q_dot, q_ddot)
    validate_state(x_dot)
    return x_dot