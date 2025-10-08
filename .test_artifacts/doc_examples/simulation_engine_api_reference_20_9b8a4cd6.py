# Example from: docs\api\simulation_engine_api_reference.md
# Index: 20
# Runnable: True
# Hash: 9b8a4cd6

self.dynamics_model: Any              # Dynamics model instance
self.dt: float                        # Integration timestep
self.max_time: float                  # Maximum simulation time
self.current_time: float              # Current simulation time (updated after run)
self.step_count: int                  # Number of steps executed (updated after run)
self.simulation_history: List[dict]   # History of all simulation runs