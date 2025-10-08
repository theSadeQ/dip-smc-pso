# Example from: docs\api\factory_system_api_reference.md
# Index: 59
# Runnable: False
# Hash: 9128def7

# example-metadata:
# runnable: false

# src/controllers/new_controller.py

import numpy as np
from typing import Dict, List, Any
from numpy.typing import NDArray

class NewController:
    """New controller implementation."""

    def __init__(self, gains: List[float], max_force: float, dt: float, **kwargs):
        """Initialize new controller.

        Args:
            gains: Controller gains [g1, g2, g3, ...]
            max_force: Maximum control force [N]
            dt: Sampling time [s]
        """
        self._gains = gains
        self.max_force = max_force
        self.dt = dt
        # Additional initialization...

    def compute_control(
        self,
        state: NDArray[np.float64],
        last_control: float,
        history: Dict[str, Any]
    ) -> Any:
        """Compute control output."""
        # Controller logic...
        u = 0.0  # Compute control

        # Saturation
        u = np.clip(u, -self.max_force, self.max_force)

        # Return control output (can be dict, float, or structured result)
        return {'u': u, 'status': 'ok'}

    def reset(self) -> None:
        """Reset controller state."""
        # Reset internal state...
        pass

    @property
    def gains(self) -> List[float]:
        """Return controller gains."""
        return self._gains.copy()