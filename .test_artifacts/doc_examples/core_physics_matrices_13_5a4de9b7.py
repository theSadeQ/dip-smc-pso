# Example from: docs\reference\plant\core_physics_matrices.md
# Index: 13
# Runnable: True
# Hash: 5a4de9b7

def warmup_physics_computer(physics):
    """Pre-compile Numba functions."""
    dummy_state = np.zeros(6)
    physics.compute_inertia_matrix(dummy_state)
    physics.compute_coriolis_matrix(dummy_state)
    physics.compute_gravity_vector(dummy_state)