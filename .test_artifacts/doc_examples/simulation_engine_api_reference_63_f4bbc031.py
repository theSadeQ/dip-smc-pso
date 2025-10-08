# Example from: docs\api\simulation_engine_api_reference.md
# Index: 63
# Runnable: True
# Hash: f4bbc031

self.states: Optional[np.ndarray]     # State trajectory (n_steps+1, state_dim)
self.times: Optional[np.ndarray]      # Time vector (n_steps+1,)
self.controls: Optional[np.ndarray]   # Control sequence (n_steps,)
self.metadata: Dict[str, Any]         # Additional data