# Example from: docs\api\simulation_engine_api_reference.md
# Index: 22
# Runnable: True
# Hash: 083576fb

{
    'success': bool,              # Whether simulation completed without error
    'states': np.ndarray,         # State trajectory (n_steps+1, state_dim)
    'controls': np.ndarray,       # Control sequence (n_steps,)
    'time': np.ndarray,           # Time vector (n_steps+1,)
    'final_state': np.ndarray,    # Final state (state_dim,)
    'step_count': int,            # Number of steps executed
    'error': str                  # Error message (only if success=False)
}