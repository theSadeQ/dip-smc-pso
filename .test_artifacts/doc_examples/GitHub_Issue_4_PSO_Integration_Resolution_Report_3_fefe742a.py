# Example from: docs\GitHub_Issue_4_PSO_Integration_Resolution_Report.md
# Index: 3
# Runnable: True
# Hash: fefe742a

# Enhanced factory with PSO-specific interface
from enum import Enum
from typing import Protocol, Union, List, Optional, Tuple
import numpy as np

class SMCType(Enum):
    """Enumeration of SMC controller types for PSO optimization."""
    CLASSICAL = "classical_smc"
    ADAPTIVE = "adaptive_smc"
    SUPER_TWISTING = "sta_smc"
    HYBRID = "hybrid_adaptive_sta_smc"

class PSOControllerWrapper:
    """PSO-friendly wrapper that simplifies control interface."""

    def __init__(self, controller: Any):
        self.controller = controller
        self._history = {}

        # Initialize appropriate state_vars based on controller type
        controller_name = type(controller).__name__
        if 'SuperTwisting' in controller_name or 'STA' in controller_name:
            self._state_vars = (0.0, 0.0)  # (z, sigma)
        elif 'Hybrid' in controller_name:
            self._state_vars = (4.0, 0.4, 0.0)  # (k1_init, k2_init, u_int_prev)
        else:
            self._state_vars = ()  # Classical and Adaptive

    def compute_control(self, state: np.ndarray, state_vars=None, history=None):
        """
        Flexible interface supporting both:
        1. compute_control(state) - PSO-friendly simplified
        2. compute_control(state, state_vars, history) - Full interface
        """
        final_state_vars = state_vars if state_vars is not None else self._state_vars
        final_history = history if history is not None else self._history

        result = self.controller.compute_control(state, final_state_vars, final_history)

        # For PSO usage, return numpy array
        if state_vars is None and history is None:
            if hasattr(result, 'u'):
                control_value = result.u
            elif isinstance(result, dict) and 'u' in result:
                control_value = result['u']
            elif isinstance(result, tuple) and len(result) > 0:
                control_value = result[0]
            else:
                control_value = result

            # Ensure numpy array output
            if isinstance(control_value, (int, float)):
                return np.array([control_value])
            elif isinstance(control_value, np.ndarray):
                return control_value.flatten()
            else:
                return np.array([float(control_value)])
        else:
            return result