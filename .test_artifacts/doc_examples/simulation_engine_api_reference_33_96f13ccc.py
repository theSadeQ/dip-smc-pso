# Example from: docs\api\simulation_engine_api_reference.md
# Index: 33
# Runnable: False
# Hash: 96f13ccc

def validate_state(self, state: np.ndarray) -> bool:
    """Validate state vector using configured validator."""
    if hasattr(self, '_state_validator'):
        return self._state_validator.validate_state(state)
    return self._basic_state_validation(state)

def sanitize_state(self, state: np.ndarray) -> np.ndarray:
    """Sanitize state vector if validator supports it."""
    if hasattr(self, '_state_validator'):
        return self._state_validator.sanitize_state(state)
    return state