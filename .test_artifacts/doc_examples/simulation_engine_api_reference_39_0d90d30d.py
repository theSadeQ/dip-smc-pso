# Example from: docs\api\simulation_engine_api_reference.md
# Index: 39
# Runnable: True
# Hash: 0d90d30d

def get_physics_matrices(
    self,
    state: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Get simplified physics matrices M, C, G."""