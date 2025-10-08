# Example from: docs\api\simulation_engine_api_reference.md
# Index: 41
# Runnable: False
# Hash: 978533fc

def compute_dynamics(
    self,
    state: np.ndarray,
    control_input: np.ndarray,
    time: float = 0.0,
    **kwargs: Any
) -> DynamicsResult:
    """Compute linear dynamics: ẋ = Ax + Bu"""
    state_derivative = self.A @ state + self.B @ control_input

    # Optional time-varying disturbance
    if hasattr(self, '_compute_time_varying_terms'):
        disturbance = self._compute_time_varying_terms(time, state)
        state_derivative += disturbance

    return DynamicsResult.success_result(state_derivative, time=time)