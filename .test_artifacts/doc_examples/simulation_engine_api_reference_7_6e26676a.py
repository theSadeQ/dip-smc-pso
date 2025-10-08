# Example from: docs\api\simulation_engine_api_reference.md
# Index: 7
# Runnable: True
# Hash: 6e26676a

Tuple[np.ndarray, np.ndarray, np.ndarray]
    t_arr : np.ndarray  # Time vector (n_steps+1,)
    x_arr : np.ndarray  # State trajectory (n_steps+1, state_dim)
    u_arr : np.ndarray  # Control sequence (n_steps,)