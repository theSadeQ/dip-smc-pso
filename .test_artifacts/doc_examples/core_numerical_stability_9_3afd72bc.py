# Example from: docs\reference\plant\core_numerical_stability.md
# Index: 9
# Runnable: True
# Hash: 3afd72bc

# Dynamics computation: M(q)q̈ = τ - C·q̇ - G
M = physics.compute_inertia_matrix(state)
forcing = tau - C @ q_dot - G

# Solve for accelerations (preferred method)
q_ddot = inverter.solve_linear_system(M, forcing)

# Equivalent but slower:
# M_inv = inverter.invert_matrix(M)
# q_ddot = M_inv @ forcing