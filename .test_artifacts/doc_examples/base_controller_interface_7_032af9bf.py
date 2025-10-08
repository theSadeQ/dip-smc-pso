# Example from: docs\reference\controllers\base_controller_interface.md
# Index: 7
# Runnable: False
# Hash: 032af9bf

# example-metadata:
# runnable: false

def compute_control(
    self,
    state: np.ndarray,
    state_vars: Dict[str, Any],
    history: Dict[str, Any]
) -> Tuple[float, Dict[str, Any], Dict[str, Any]]:
    # Extract previous state
    K = state_vars.get('K', self.K_initial)

    # Update state (e.g., adaptation)
    K_new = K + self.gamma * abs(s) * self.dt

    # Return new state
    return u, {'K': K_new}, history